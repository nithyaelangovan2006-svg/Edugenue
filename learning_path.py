from config import ask_gemini


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured, adaptive learning path with key topics, order of learning,
estimated time for each stage, and resources (videos, articles, books).
Include beginner, intermediate, and advanced levels. Use Markdown headings and bullet lists."""
    return ask_gemini(prompt)
