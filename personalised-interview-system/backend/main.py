from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.database import init_db
from backend.api import resume, interview

app = FastAPI(title="Personalised Interview Preparation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(resume.router, prefix="/api/resume")
app.include_router(interview.router, prefix="/api/interview")


@app.get("/api/health")
def health():
    return {"status": "ok"}
