# models.py
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from config import GEMINI_MODEL

def load_embedder():
    return SentenceTransformer(
        "nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True
    )

def load_llm(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(GEMINI_MODEL)
