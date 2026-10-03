from config import ask_gemini


def answer_question_with_gemini(question: str) -> str:
    prompt = f"You are a helpful tutor. Answer clearly and concisely:\n\n{question}"
    return ask_gemini(prompt)
