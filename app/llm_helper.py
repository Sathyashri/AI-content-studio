from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st

# -------------------------------
# LOAD ENV
# -------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

# -------------------------------
# LOAD CLIENT (CACHED)
# -------------------------------
@st.cache_resource
def load_client():
    return Groq(api_key=api_key)

client = load_client()

# -------------------------------
# GENERATE FUNCTION
# -------------------------------
def generate_from_llm(prompt):

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional AI content writer. Give clean output without unnecessary explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating content: {str(e)}"