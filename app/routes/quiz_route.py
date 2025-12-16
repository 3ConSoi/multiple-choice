from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/random")
def get_random_questions():
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, text, choices, answer_key FROM questions ORDER BY RANDOM() LIMIT 20;"
        )).mappings().all()

    # convert từ Row → dict để frontend hiểu
    questions = []
    for r in rows:
        questions.append({
            "id": r["id"],
            "text": r["text"],
            "choices": r["choices"],
            "answer_key": r["answer_key"]
        })
    return questions
