from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class Choice(BaseModel):
    id: str
    label: str

class QuestionCreate(BaseModel):
    text: str
    choices: List[Choice]
    answer_key: List[str]
    difficulty: Optional[str] = "medium"
    category_id: Optional[int] = None

class QuestionOut(BaseModel):
    id: int
    text: str
    choices: List[Choice]
    difficulty: str
    category_id: Optional[int]

class ExamCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    duration_min: Optional[int] = 30
    question_ids: List[int] = []

class ExamOut(BaseModel):
    id: int
    title: str
    description: str
    duration_min: int

class StartAttemptResponse(BaseModel):
    attempt_id: int
    exam_id: int
    started_at: datetime
    duration_sec: int
    questions: List[QuestionOut]

class SubmitPayload(BaseModel):
    attempt_id: int
    answers: dict  # question_id -> list of choice ids

class SubmitResult(BaseModel):
    attempt_id: int
    score: int
    total: int
    per_question: dict
    passed: bool