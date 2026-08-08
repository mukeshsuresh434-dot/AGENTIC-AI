from pydantic import BaseModel
from typing import Optional


class InterviewCreate(BaseModel):
    candidate_id: int
    interview_type: str = "mixed"
    difficulty: str = "adaptive"
    total_questions: int = 10


class InterviewStatus(BaseModel):
    session_id: int
    current_question: int
    total_questions: int
    status: str
