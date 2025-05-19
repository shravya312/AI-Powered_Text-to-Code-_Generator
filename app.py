from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Retrieve Gemini API key
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Text to Code Generator", layout="centered")
st.title("🧠 Text to Code Generator using Gemini")
st.write("Describe what your code should do, and let AI generate the code!")

# User input
prompt = st.text_area("💬 Describe the code (e.g., 'add 2 numbers')")

if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("Generating code..."):
            try:
                # Use a valid Gemini model name (update as needed)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"Generate Python code for the following task:\n{prompt}"
                )
                # Some Gemini responses may return a list of candidates
                code = response.text if hasattr(response, "text") else str(response)
                st.success("✅ Code generated successfully!")
                st.code(code, language="python")
            except Exception as e:
                st.error(f"Error: {e}")
