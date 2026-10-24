# llm/gemini_client.py
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

def call_gemini(prompt: str):
    return model.generate_content(prompt).text
