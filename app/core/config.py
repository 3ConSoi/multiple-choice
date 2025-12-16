import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost:5432/quizdb")
# configurable quiz defaults
DEFAULT_EXAM_DURATION_MIN = int(os.getenv("DEFAULT_EXAM_DURATION_MIN", "30"))