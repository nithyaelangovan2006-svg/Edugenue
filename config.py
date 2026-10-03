"""Shared Gemini client used by every cloud-powered module."""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
_client = None


def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text reply."""
    global _client
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Copy .env.example to .env and add your key.")
    if _client is None:
        _client = genai.Client(api_key=API_KEY)
    response = _client.models.generate_content(model=MODEL, contents=prompt)
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
