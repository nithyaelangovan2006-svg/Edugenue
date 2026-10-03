from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="EduGenie")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def fail(error: Exception, status: int = 500):
    return JSONResponse(content={"error": str(error)}, status_code=status)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


# Q&A - GET
@app.get("/qa")
async def answer_question(question: str = Query(..., min_length=1)):
    try:
        return {"answer": answer_question_with_gemini(question)}
    except Exception as e:
        return fail(e)


# Explanation - POST
@app.post("/explain/")
async def explain_api(request: Request):
    data = await request.json()
    topic = (data.get("topic") or "").strip()
    if not topic:
        return fail(ValueError("Please provide a topic."), 400)
    try:
        return {"topic": topic, "explanation": explain_topic(topic)}
    except Exception as e:
        return fail(e)


# Summarization - POST
@app.post("/summarize/")
async def summarize_api(request: Request):
    data = await request.json()
    text = (data.get("text") or "").strip()
    if not text:
        return fail(ValueError("Please provide text to summarize."), 400)
    try:
        return {"summary": summarize_text(text)}
    except Exception as e:
        return fail(e)


# Quiz generation - POST
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = (data.get("text") or "").strip()
    if not text:
        return fail(ValueError("Please provide a topic or text for the quiz."), 400)
    try:
        return {"quiz": generate_quiz(text)}
    except Exception as e:
        return fail(e)


# Learning recommendations - GET
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(..., min_length=1)):
    try:
        return {"topic": topic, "recommendation": get_learning_recommendations(topic)}
    except Exception as e:
        return fail(e)
