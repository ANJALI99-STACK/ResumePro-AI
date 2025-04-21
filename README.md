## **Project Overview**

**ResumePro AI** is an AI-powered web application designed to assist job seekers in enhancing their resumes and matching them with job descriptions. Built using Streamlit and Gemini AI, this application provides features such as resume analysis, ATS score evaluation, job description matching, and real-time job search from LinkedIn.

## **Features**

- **Resume Analyzer**: Upload your resume to receive instant AI-powered suggestions, ATS scores, and section-wise improvements.

- **Section-wise Suggestions**: Get targeted feedback for each resume section.
  
- **Job Description Match**: Compare your resume with specific job descriptions to see how well they align and receive tailored summaries and rewrites.

- **Tailored Resume Summary**: Generate a custom summary based on the job.

- **Real-Time LinkedIn Job Search**: Search for open job roles by title and view job cards fetched directly from LinkedIn.

- **AI Resume Rewriter**: Enhance your resume with AI-generated improvements.

- **ATS Compatibility Score**: Check how well your resume is optimized for Applicant Tracking Systems.

- **PDF Export**: Download analysis reports, summaries, and improved resumes as PDFs.


## **Installation**

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ANJALI99-STACK/ResumePro-AI.git
   cd ResumePro-AI

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up your environment variables. Create a .env file in the root directory and add your Gemini API key:**
   GEMINI_API_KEY=your_api_key_here
5. **Run the application**
   ```bash
   streamlit run app.py

## Usage

- **Upload Resume**: Use the "Resume Analyzer" tab to upload your resume and get instant feedback.
- **Match with Job Description**: In the "Job Description Match" tab, upload both your resume and a job description to see how they compare.
- **Search Jobs**: Use the "LinkedIn Job Search" tab to find job openings by entering a job title.
- **About Section**: Learn more about the application and its features in the "About" tab.

## Technologies Used

- **Streamlit**: For building the web application interface.
- **Gemini AI**: For AI-powered analysis and suggestions.
- **Python**: The primary programming language used.
- **Various Libraries**: Including dotenv, os, re, and others for functionality.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries, please reach out to Anjali.




