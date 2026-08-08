from pydantic import BaseModel
from typing import Optional


class QuestionOut(BaseModel):
    id: int
    category: Optional[str]
    question_text: str
    difficulty: Optional[str]
    topic: Optional[str]

    class Config:
        orm_mode = True
