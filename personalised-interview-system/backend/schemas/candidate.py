from pydantic import BaseModel
from typing import Optional, List


class CandidateProfile(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str] = []
    programming_languages: List[str] = []
    frameworks: List[str] = []
    projects: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None


class CandidateCreate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    resume_text: Optional[str]
