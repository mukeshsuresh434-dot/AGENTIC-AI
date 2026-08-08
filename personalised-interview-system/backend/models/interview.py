from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.init_db import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    interview_type = Column(String, default="mixed")
    difficulty = Column(String, default="adaptive")
    total_questions = Column(Integer, default=10)
    current_question = Column(Integer, default=0)
    status = Column(String, default="in_progress")
    overall_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate")
