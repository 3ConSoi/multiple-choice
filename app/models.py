from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import JSON

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    meta = Column("meta", String)
    text = Column(Text, nullable=False)
    choices = Column(JSON, nullable=False)  # list of {id,label}
    answer_key = Column(JSON, nullable=False)  # list of correct choice ids (supports multi-select)
    difficulty = Column(String, default="medium")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")

class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_min = Column(Integer, default=30)  # exam duration

class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    duration_sec = Column(Integer, nullable=True)  # actual duration used
    score = Column(Integer, nullable=True)
    extra = Column(JSON, default={})  # e.g., per-question result, user info

class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_answer = Column(String(10), nullable=False)