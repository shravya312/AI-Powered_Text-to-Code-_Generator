from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

# Load environment variables
# load_dotenv(dotenv_path=".env")

# Retrieve Gemini API key
api_key = os.getenv("GEMINI_API_KEY", "").strip()

# Retrieve API key with priority: Streamlit Secrets > .env > empty string
api_key = (
    st.secrets.get("GEMINI_API_KEY")  # First try Streamlit Secrets (for deployment)
    or os.getenv("GEMINI_API_KEY", "").strip()  # Then check .env (for local dev)
)
if not api_key:
    st.error("""
    Gemini API key not found. Please:
    1. For deployment: Add GEMINI_API_KEY in Streamlit Cloud Secrets (app settings ⚙️)
    2. For local dev: Create `.env` file with GEMINI_API_KEY=your_key
    """)
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Text to Code Generator", layout="centered")
st.title("🧠 Text to Code Generator using Gemini")
st.write("Describe what your code should do, select a programming language, and let AI generate the code!")

# User input
prompt = st.text_area("💬 Describe the code (e.g., 'add 2 numbers')")

# Language selection, now including SQL
languages = [
    "Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "PHP",
    "TypeScript", "Swift", "Kotlin", "Rust", "SQL"
]
language = st.selectbox("📝 Select programming language", languages, index=0)

if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a description.")
    else:
        with st.spinner("Generating code..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                system_prompt = (
                    f"You are an expert {language} developer. "
                    "Write clean, efficient, and well-documented code following best practices. "
                    f"Generate {language} code for the following task:\n{prompt}"
                )
                response = model.generate_content(system_prompt)
                code = response.text if hasattr(response, "text") else str(response)
                # For Streamlit code highlighting, use 'sql' for SQL, else language.lower()
                code_lang = "sql" if language.lower() == "sql" else language.lower()
                st.success("✅ Code generated successfully!")
                st.code(code, language=code_lang)
            except Exception as e:
                st.error(f"Error: {e}")
