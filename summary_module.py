from config import ask_gemini


def summarize_text(text: str) -> str:
    prompt = f"Summarize the following text in simple language, keeping the key points:\n\n{text}"
    return ask_gemini(prompt)
