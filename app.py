# --- Imports ---
import streamlit as st
import os
import re
from parser import parse_resume
from analyzer import (
    analyze_with_ai,
    get_ats_score,
    compare_with_job_description,
    generate_tailored_summary,
    get_section_wise_suggestions,
    rewrite_resume,
    rewrite_resume_with_ai,
    highlight_resume_vs_jd,
)
from scraper import scrape_linkedin_jobs
from util import generate_pdf, generate_text_pdf
from dotenv import load_dotenv

load_dotenv()

# --- Page Setup ---
st.set_page_config(page_title="ResumePro AI — Your Smart Career Companion", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6em 2em;
        margin-bottom: 1em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a6ed8;
    }
    .stExpander {
        border-radius: 8px;
        border: 1px solid #4F8BF9;
        margin-bottom: 1em;
        padding: 0.5em 1em;
    }
    .big-font {
        font-size: 32px !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2em;
    }
    .centered {
        text-align: center;
    }
    .file-upload-label {
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 0.5em;
    }
    .job-card {
        border: 1px solid #4F8BF9;
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 1em;
        background-color: #f9fbff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<p class="big-font centered">ResumePro AI — Your Smart Career Companion</p>', unsafe_allow_html=True)
st.caption("Built with Gemini AI + Streamlit | Resume Rewrite • ATS Score • JD Match • LinkedIn Search")
st.divider()

# --- Tabs ---
tab_resume, tab_jd_match, tab_jobs, tab_about = st.tabs(
    ["Resume Analyzer", "Job Description Match", "LinkedIn Job Search", "About"]
)

# -------------------------------
# Tab: Resume Analyzer
# -------------------------------
with tab_resume:
    st.markdown("### Upload and Analyze Your Resume")
    st.markdown("Get instant AI-powered suggestions, ATS score, and section-wise improvements.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="file-upload-label">Upload Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], label_visibility="collapsed")

    if uploaded_file:
        os.makedirs("resumes", exist_ok=True)
        file_path = os.path.join("resumes", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Resume uploaded successfully!")

        with st.spinner("Parsing your resume..."):
            resume_text = parse_resume(file_path)

        with st.expander("Resume Preview", expanded=False):
            st.markdown("##### Parsed Resume Content")
            st.text_area("Parsed Resume", resume_text, height=300, label_visibility="collapsed")

        with st.expander("AI Resume Rewriter", expanded=False):
            if st.button("Rewrite Resume with AI"):
                with st.spinner("Rewriting your resume..."):
                    improved_resume = rewrite_resume_with_ai(resume_text)
                st.markdown("#### AI-Enhanced Resume")
                st.text_area("Improved Resume", improved_resume, height=300)

        with st.spinner(" Analyzing with Gemini AI..."):
            analysis = analyze_with_ai(resume_text)

        with st.expander("AI Analysis", expanded=True):
            st.markdown("#### Smart Insights from Gemini")
            st.write(analysis)

        with st.expander("Section-wise Suggestions", expanded=False):
            if st.button("Get Section Suggestions"):
                with st.spinner("Reviewing each section..."):
                    section_suggestions = get_section_wise_suggestions(resume_text)
                st.markdown("#### Suggestions to Improve")
                st.markdown(section_suggestions)

        with st.expander("ATS Compatibility Score", expanded=True):
            score, issues = get_ats_score(resume_text)
            st.metric(label="Estimated ATS Score", value=f"{score}/100")
            if issues:
                st.markdown("#### Suggestions:")
                for issue in issues:
                    st.write(f"- {issue}")
            else:
                st.success("Your resume looks ATS-friendly!")

        if st.button("Download Analysis as PDF"):
            if analysis:
                pdf_file = generate_pdf(analysis)
                st.download_button("Download PDF", pdf_file, file_name="resume_analysis.pdf")

# -------------------------------
# Tab: Job Description Match
# -------------------------------
with tab_jd_match:
    st.markdown("###  Match Your Resume with a Job Description")
    st.markdown("See how well your resume aligns with a specific job and get AI-generated summaries and rewrites.")

    st.markdown('<div class="file-upload-label">Upload Resume and Job Description</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"], key="res_jd")
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"], key="jd_jd")

    if resume_file and jd_file:
        os.makedirs("resumes", exist_ok=True)
        resume_path = os.path.join("resumes", resume_file.name)
        jd_path = os.path.join("resumes", jd_file.name)
        with open(resume_path, "wb") as f1, open(jd_path, "wb") as f2:
            f1.write(resume_file.read())
            f2.write(jd_file.read())

        resume_text = parse_resume(resume_path)
        job_description_text = parse_resume(jd_path)

        with st.spinner("Comparing Resume with Job Description..."):
            highlighted_resume, keywords = highlight_resume_vs_jd(resume_text, job_description_text)

        with st.expander("Resume vs Job Description (with Highlights)", expanded=True):
            st.markdown("#### Keywords Matched in Resume")
            st.markdown(", ".join(keywords))
            st.markdown("#### Highlighted Resume")
            st.markdown(highlighted_resume, unsafe_allow_html=True)

        with st.expander("Tailored Resume Summary (AI Generated)", expanded=False):
            tailored_summary = generate_tailored_summary(resume_text, job_description_text)
            st.code(tailored_summary, language="markdown")
            if tailored_summary:
                summary_pdf = generate_text_pdf("Tailored Resume Summary", tailored_summary)
                st.download_button(
                    label="Download Summary as PDF",
                    data=summary_pdf,
                    file_name="tailored_summary.pdf",
                    mime="application/pdf"
                )

        with st.expander("Rewrite Resume with AI", expanded=False):
            if st.button("Generate Improved Resume"):
                with st.spinner(" Rewriting resume with Gemini AI..."):
                    improved_resume = rewrite_resume(resume_text, job_description_text)
                st.text_area("Rewritten Resume (AI)", improved_resume, height=300, label_visibility="collapsed")
                if improved_resume:
                    improved_pdf = generate_text_pdf("Improved Resume", improved_resume)
                    st.download_button(
                        label=" Download Rewritten Resume",
                        data=improved_pdf,
                        file_name="improved_resume.pdf",
                        mime="application/pdf"
                    )

# -------------------------------
# Tab: LinkedIn Job Search
# -------------------------------
with tab_jobs:
    st.markdown("### Real-Time LinkedIn Job Search")
    st.markdown("Search open roles by title and view job cards fetched directly from LinkedIn.")

    job_query = st.text_input("Enter Job Title (e.g., Data Scientist, Frontend Developer)")

    if job_query:
        with st.spinner("Searching LinkedIn Jobs..."):
            job_results = scrape_linkedin_jobs(job_query)

        if job_results:
            for job in job_results:
                st.markdown(f'<div class="job-card">', unsafe_allow_html=True)
                st.markdown(f"### {job['title']}")
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"[Job Link]({job['link']})")
                st.markdown(f"**Description:** {job['description'][:200]}...")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No jobs found for this query. Try again later!")

# -------------------------------
# Tab: About
# -------------------------------
with tab_about:
    st.markdown("## What is ResumePro AI?")
    st.markdown("""
**ResumePro AI** is your AI-powered job search partner, built to help you stand out in the competitive hiring landscape.

With the power of Gemini AI and intuitive design, it helps you:

- Improve and rewrite your resume with smart suggestions  
- Check how well your resume scores for Applicant Tracking Systems (ATS)  
- Compare your resume with job descriptions to see what’s missing  
- Get tailored resume summaries for specific roles  
- Find real-time job opportunities directly from LinkedIn  
- Export reports and AI-enhanced resumes as PDFs  
    """)
    st.markdown("---")
    st.markdown("Made by [Anjali](https://github.com/ANJALI99-STACK)")

# Footer
st.divider()
