import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug: Check if key is loaded (remove in production)
api_key = os.environ.get("OPENAI_API_KEY")
PROJECT_ID = os.environ.get("OPENAI_PROJECT_ID")
if not api_key:
    st.error("OPENAI_API_KEY not found in .env file!")
    st.stop()

# Print first/last few chars for debugging (safe)
st.write("API Key loaded:", api_key[:8] + "..." + api_key[-4:] if api_key else "None")

# Initialize client
client = OpenAI(
    api_key=api_key,
    project=PROJECT_ID
)

st.set_page_config(page_title="English ↔ Somali Translator", page_icon="🌍")

st.title("English ↔ Somali Translator")
st.write("Translate text between English and Somali using GPT-4o-mini.")

direction = st.selectbox(
    "Choose translation direction:",
    ["English → Somali", "Somali → English"]
)

text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if not text_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                if direction == "English → Somali":
                    prompt = f"Translate the following English text to Somali. Only respond with the translation, no explanations:\n\n{text_input}"
                else:
                    prompt = f"Translate the following Somali text to English. Only respond with the translation, no explanations:\n\n{text_input}"

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )

                translation = response.choices[0].message.content.strip()

                st.subheader("Translation:")
                st.success(translation)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                if "authentication" in str(e).lower() or "401" in str(e):
                    st.error("Your OpenAI API key is invalid or expired. Please check it at https://platform.openai.com/api-keys")