"""Concept explanations with the local LaMini-Flan-T5-783M model.
The model loads on the first request (~3 GB download once). If it cannot be loaded,
the module falls back to Gemini so the feature keeps working."""
from config import ask_gemini

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"
_tokenizer = None
_model = None


def _load():
    global _tokenizer, _model
    if _model is None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return _tokenizer, _model


def explain_topic(topic: str) -> str:
    prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    try:
        tokenizer, model = _load()
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs, max_new_tokens=200, temperature=0.7, top_k=50, top_p=0.95, do_sample=True
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as local_error:
        print(f"[explain] Local model unavailable ({local_error}); using Gemini.")
        return ask_gemini(prompt)
