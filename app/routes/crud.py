from sqlalchemy.orm import Session
from app import models
from typing import List
import random
from datetime import datetime, timedelta

def create_question(db: Session, q):
    obj = models.Question(
        text=q.text,
        choices=[c.dict() for c in q.choices],
        answer_key=q.answer_key,
        difficulty=q.difficulty,
        category_id=q.category_id
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.post("/seed")
def seed_questions(db: Session = Depends(get_db)):
    with open("seed_questions.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    db.execute(text(sql))
    db.commit()
    return {"message": "Seed questions successfully"}

def get_questions(db: Session, category_id=None, difficulty=None):
    q = db.query(models.Question)
    if category_id:
        q = q.filter(models.Question.category_id == category_id)
    if difficulty:
        q = q.filter(models.Question.difficulty == difficulty)
    return q.all()

def create_exam(db: Session, exam_in):
    exam = models.Exam(title=exam_in.title, description=exam_in.description, duration_min=exam_in.duration_min)
    db.add(exam); db.commit(); db.refresh(exam)
    for qid in exam_in.question_ids:
        eq = models.ExamQuestion(exam_id=exam.id, question_id=qid)
        db.add(eq)
    db.commit()
    return exam

def start_attempt(db: Session, exam_id: int, num_questions: int = None, randomize: bool = True, filters: dict = None):
    exam = db.query(models.Exam).filter(models.Exam.id == exam_id).first()
    if not exam:
        return None
    # gather question ids for exam
    qids = [eq.question_id for eq in db.query(models.ExamQuestion).filter(models.ExamQuestion.exam_id == exam_id).all()]
    questions = db.query(models.Question).filter(models.Question.id.in_(qids)).all()
    if filters:
        if filters.get("category_id"):
            questions = [qq for qq in questions if qq.category_id == filters["category_id"]]
        if filters.get("difficulty"):
            questions = [qq for qq in questions if qq.difficulty == filters["difficulty"]]
    if randomize:
        random.shuffle(questions)
    if num_questions:
        questions = questions[:num_questions]
    attempt = models.Attempt(exam_id=exam.id, duration_sec=exam.duration_min * 60)
    db.add(attempt); db.commit(); db.refresh(attempt)
    # pack questions into metadata so we know the order presented
    attempt.metadata = {"question_order": [q.id for q in questions], "per_question": {}}
    db.add(attempt); db.commit(); db.refresh(attempt)
    return attempt, questions, exam

def grade_attempt(db: Session, attempt_id: int, answers: dict, pass_threshold_percent: int = 50):
    attempt = db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()
    if not attempt:
        return None
    q_order = attempt.metadata.get("question_order", [])
    per_q = {}
    correct = 0
    total = len(q_order)
    for qid in q_order:
        q = db.query(models.Question).filter(models.Question.id == qid).first()
        provided = answers.get(str(qid), [])
        # normalize both lists
        if set(provided) == set(q.answer_key):
            per_q[str(qid)] = {"correct": True, "expected": q.answer_key, "given": provided}
            correct += 1
        else:
            per_q[str(qid)] = {"correct": False, "expected": q.answer_key, "given": provided}
    score = int((correct / total) * 100)
    attempt.score = score
    attempt.finished_at = datetime.utcnow()
    attempt.metadata["per_question"] = per_q
    db.add(attempt); db.commit(); db.refresh(attempt)
    passed = score >= pass_threshold_percent
    return {"attempt_id": attempt.id, "score": score, "total": total, "per_question": per_q, "passed": passed}
