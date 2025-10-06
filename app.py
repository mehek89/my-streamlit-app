import streamlit as st
import os
from google import genai
from google.genai import types

# --- API KEY RETRIEVAL LOGIC ---
# This must be at the very top of your script.
API_KEY = None
try:
    # 1. Try to get the key from Streamlit's secrets manager (.streamlit/secrets.toml)
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    # 2. Fallback to check a regular OS environment variable
    API_KEY = os.getenv("GEMINI_API_KEY")

# Stop the app if the key is not found
if not API_KEY:
    st.error("GEMINI_API_KEY environment variable not set. Please set it to run the app in `.streamlit/secrets.toml` or as an OS variable.")
    st.stop()
    
# --- CONSTANTS AND SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are an expert AI code generator. Your task is to ONLY output the raw, complete, and correct code based on the user's request. 
DO NOT include any conversational text, explanations, markdown headings, or commentary before or after the code block. 
If the user asks for an HTML page, ONLY output the HTML code starting with `<!DOCTYPE html>`.
If the user asks for a Python script, ONLY output the Python code.
Ensure the code is syntactically correct and ready to run.
"""
@st.cache_data
def generate_code(prompt_text, api_key):
    """Interacts with the Gemini API to generate code."""
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt_text],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, 
                temperature=0.2, 
            )
        )
        
        return response.text.strip()
        
    except Exception as e:
        return f"An error occurred: {e}"
# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="Gemini Code Generator",
    layout="centered"
)

st.title("✨ Gemini Code Generator")
st.caption("Ask me to generate a script, function, or HTML/CSS code.")
st.divider()

# --- Get User Input ---
prompt = st.text_area(
    "What kind of code do you want to generate?",
    placeholder="e.g., 'A Python function to calculate the Fibonacci sequence up to 10 terms.'",
    height=150
)

# --- Create the Submit Button ---
if st.button("Generate Code", use_container_width=True) and prompt:
    # --- Loading State and API Call ---
    with st.spinner("🧑‍💻 Generating code... Please wait."):
        
        # Pass the correctly defined API_KEY variable
        generated_text = generate_code(prompt, API_KEY) 
        
        # --- Display Result ---
        st.subheader("Generated Code")
        
        # Use st.code to display the output with syntax highlighting
        # The 'python' language is a safe default for general code generation
        st.code(generated_text, language="python", line_numbers=True)

# Add a simple instruction at the end
st.info("Remember to check the generated code for correctness and security before use.")