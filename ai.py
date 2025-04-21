import google.generativeai as genai
import os

# Load your API key from environment variable or directly (not recommended to hardcode)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_gemini_api(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini API: {str(e)}"
