from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
from fpdf import FPDF
from io import BytesIO




def generate_pdf(analysis_text, file_name="resume_analysis.pdf"):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "📄 AI Resume Analysis Report")

    # Add some space
    c.setFont("Helvetica", 12)
    text_object = c.beginText(40, height - 80)
    text_object.setLeading(16)  # Line spacing

    # Split the analysis into lines and wrap long lines
    lines = analysis_text.splitlines()
    max_width = width - 80  # right margin

    for line in lines:
        while line:
            if c.stringWidth(line, "Helvetica", 12) < max_width:
                text_object.textLine(line)
                break
            else:
                # Wrap the line manually
                cutoff = len(line)
                while c.stringWidth(line[:cutoff], "Helvetica", 12) > max_width:
                    cutoff -= 1
                split_point = line.rfind(" ", 0, cutoff)
                if split_point == -1:
                    split_point = cutoff
                text_object.textLine(line[:split_point])
                line = line[split_point:].lstrip()

        # Move to next page if needed
        if text_object.getY() < 50:
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText(40, height - 50)
            text_object.setLeading(16)
            c.setFont("Helvetica", 12)

    c.drawText(text_object)
    c.showPage()
    c.save()
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(40, 30, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return file_name



def generate_text_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=title, align="L")
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt=content, align="L")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output = BytesIO(pdf_bytes)
    return pdf_output

