import json
import re

from config import ask_gemini


def clean_json_block(text: str) -> str:
    """Strip Markdown ```json fences if the model added them."""
    return re.sub(r"```(?:json)?\s*(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    prompt = f"""You are a quiz generator.
From the following topic or passage, create 3 multiple-choice questions. Each question must include:
- "question": the question text
- "options": a list of exactly 4 answer options (plain text, no "A)" prefixes)
- "answer": the correct answer, copied exactly from one of the options

Return ONLY valid JSON, like this:
[{{"question": "What is ...?", "options": ["w", "x", "y", "z"], "answer": "x"}}]

Topic or passage:
{text}"""
    raw = clean_json_block(ask_gemini(prompt))
    try:
        quiz = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Could not parse quiz JSON: {e}. Raw output: {raw[:200]}")

    cleaned = []
    for q in quiz:
        options = [str(o) for o in q.get("options", [])]
        answer = str(q.get("answer", ""))
        if answer not in options:  # handle answers like "B" or "b"
            letter = answer.strip().upper()[:1]
            if letter in "ABCD" and letter and "ABCD".index(letter) < len(options):
                answer = options["ABCD".index(letter)]
        if len(options) >= 2 and answer in options:
            cleaned.append({"question": str(q.get("question", "")), "options": options, "answer": answer})
    if not cleaned:
        raise RuntimeError("The model returned no usable quiz questions. Please try again.")
    return cleaned
