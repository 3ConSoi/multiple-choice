from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.session import get_db
from app import crud, schemas
from typing import Optional

router = APIRouter()

@router.post("/questions", response_model=schemas.QuestionOut)
def create_question(q: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, q)

@router.get("/questions", response_model=list[schemas.QuestionOut])
def list_questions(category_id: Optional[int] = None, difficulty: Optional[str] = None, db: Session = Depends(get_db)):
    qs = crud.get_questions(db, category_id=category_id, difficulty=difficulty)
    return qs

@router.post("/exams", response_model=schemas.ExamOut)
def create_exam(exam_in: schemas.ExamCreate, db: Session = Depends(get_db)):
    exam = crud.create_exam(db, exam_in)
    return exam

@router.post("/exams/{exam_id}/start", response_model=schemas.StartAttemptResponse)
def start_exam(exam_id: int, num_questions: Optional[int] = None, randomize: Optional[bool] = True, db: Session = Depends(get_db)):
    res = crud.start_attempt(db, exam_id, num_questions=num_questions, randomize=randomize)
    if not res:
        raise HTTPException(status_code=404, detail="Exam not found")
    attempt, questions, exam = res
    # prepare QuestionOut list (but hide answer_key)
    from app.schemas import QuestionOut, Choice
    qouts = []
    for q in questions:
        qouts.append(QuestionOut(id=q.id, text=q.text, choices=q.choices, difficulty=q.difficulty, category_id=q.category_id))
    return schemas.StartAttemptResponse(
        attempt_id=attempt.id,
        exam_id=exam.id,
        started_at=attempt.started_at,
        duration_sec=attempt.duration_sec,
        questions=qouts
    )

@router.post("/attempts/submit", response_model=schemas.SubmitResult)
def submit_attempt(payload: schemas.SubmitPayload, db: Session = Depends(get_db)):
    result = crud.grade_attempt(db, payload.attempt_id, payload.answers)
    if not result:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return schemas.SubmitResult(
        attempt_id=result["attempt_id"],
        score=result["score"],
        total=result["total"],
        per_question=result["per_question"],
        passed=result["passed"]
    )