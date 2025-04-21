import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from ai import call_gemini_api  # assuming you have this utility



load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_with_ai(resume_text):
    prompt = f"""
You are a resume analysis expert.

Here is a candidate's resume content:
\"\"\"{resume_text}\"\"\"

1. Give a short summary of the candidate.
2. List their key strengths.
3. Identify any weaknesses or missing parts in the resume.
4. Suggest improvements (e.g., formatting, missing sections, or content recommendations).
5. Recommend best-fit job titles (based on experience and skills).
6. Provide any specific tips for making this resume more ATS-friendly.

Respond in a clear, structured format.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during AI analysis: {e}"

def get_ats_score(resume_text):
    score = 0
    feedback = []

    # Check presence of important sections
    required_sections = {
        "Skills": r"skills?|technical skills?",
        "Experience": r"experience|employment|work history",
        "Education": r"education|qualifications",
        "Projects": r"projects|project experience",
        "Contact": r"(email|phone|linkedin|contact)"
    }

    for section, pattern in required_sections.items():
        if re.search(pattern, resume_text, re.IGNORECASE):
            score += 15
        else:
            feedback.append(f"❌ Missing or unclear: **{section}**")

    # Keyword richness (basic estimate)
    keyword_count = len(re.findall(r"\b(Java|Python|SQL|ML|NLP|React|Node|Excel|AWS|Docker|Kubernetes)\b", resume_text, re.IGNORECASE))
    if keyword_count >= 5:
        score += 25
    elif keyword_count >= 3:
        score += 15
    else:
        feedback.append("❌ Not enough technical keywords.")

    # Score adjustments based on document length (optional feature)
    word_count = len(resume_text.split())
    if word_count < 300:
        score -= 5  # penalize for overly short resumes
    elif word_count > 1000:
        score -= 5  # penalize for overly long resumes

    final_score = min(score, 100)
    return final_score, feedback

def compare_with_job_description(resume_text, jd_text):
    prompt = f"""
You are a recruitment AI.

Compare the following **resume** with the **job description** and give:
1. A match score out of 100.
2. Matched skills and experience (mention specific keywords from the resume and job description).
3. Missing or mismatched keywords or qualifications (be specific about the gap).
4. Tips to tailor the resume more effectively for this job description.

**Resume:**
\"\"\"{resume_text}\"\"\"

**Job Description:**
\"\"\"{jd_text}\"\"\"

Respond clearly and formatted.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during comparison: {e}"

def generate_tailored_summary(resume_text, jd_text):
    prompt = f"""
You are a career coach AI.

Based on the following resume and job description, generate a custom **professional summary** (max 5 lines) for the candidate that they can use at the top of their resume or LinkedIn profile.

**Resume:**
\"\"\"{resume_text}\"\"\"

**Job Description:**
\"\"\"{jd_text}\"\"\"

Make it ATS-friendly and appealing to recruiters by highlighting the most relevant skills, experience, and achievements.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
def rewrite_resume_with_ai(resume_text):
    prompt = f"Rewrite and improve this resume to be more professional, ATS-friendly, and impactful:\n\n{resume_text}"
    try:
        response = model.generate_content(prompt)  # Use the 'model' object, not 'gemini_model'
        return response.text
    except Exception as e:
        return f"Error during resume rewriting: {e}"
def get_section_wise_suggestions(resume_text):
    prompt = (
        "You are a resume expert. Analyze the following resume and provide section-wise suggestions "
        "to improve each part (e.g., Experience, Education, Skills, Summary). "
        "Use bullet points and keep it concise:\n\n"
        f"{resume_text}"
    )
    response = model.generate_content(prompt)
    return response.text

def rewrite_resume(resume_text, job_description=None):
    prompt = f"""
You are a resume expert. Rewrite the following resume to make it more ATS-friendly, professional, and clear.

{"Also tailor it for the following job description:\n" + job_description if job_description else ""}

Resume:
{resume_text}

Give the improved version only.
"""
    return call_gemini_api(prompt)
def highlight_resume_vs_jd(resume_text, job_description_text):
    import re
    from collections import Counter

    jd_keywords = re.findall(r'\b\w+\b', job_description_text.lower())
    common_terms = [word for word, count in Counter(jd_keywords).items() if count > 1 and len(word) > 3]
    highlighted = resume_text

    for word in common_terms:
        pattern = re.compile(rf'\b({re.escape(word)})\b', re.IGNORECASE)
        highlighted = pattern.sub(r'<span style="background-color:#d1fae5;"><b>\1</b></span>', highlighted)

    return highlighted, common_terms





