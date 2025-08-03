from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

# Load environment variables (local development)
load_dotenv()

# Retrieve API key (works for both .env and Streamlit Secrets)
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API key missing! Set it in .env or Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# UI Setup
st.set_page_config(
    page_title="Text to Code Generator",
    layout="centered",
    page_icon="🧠"
)

st.title("🧠 Text to Code Generator using Gemini")
st.write("Describe your code and let AI generate it!")

# User Input
prompt = st.text_area("💬 Describe the code (e.g., 'add 2 numbers')")
languages = ["Python", "JavaScript", "Java", "C++", "SQL"]  # Shortened for brevity
language = st.selectbox("📝 Language", languages)

if st.button("Generate Code", type="primary"):  # Uses your theme's primaryColor
    if not prompt.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("Generating..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"As an expert {language} developer, write clean, efficient code for: {prompt}"
                )
                code = response.text
                st.code(code, language=language.lower())
            except Exception as e:
                st.error(f"🚨 Error: {e}")