from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes.quiz_route import router as quiz_router
from app.session import init_db

app = FastAPI(title="Multiple-choice Quiz")

templates = Jinja2Templates(directory="app/frontend")

# Init database
@app.on_event("startup")
def on_startup():
    init_db()

# Chỉ giữ 1 route cho "/"
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include API routers
app.include_router(quiz_router, prefix="/quiz")
