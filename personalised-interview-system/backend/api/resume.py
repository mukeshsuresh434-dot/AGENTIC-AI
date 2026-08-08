from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.agent.personalised_interview_agent import PersonalisedInterviewAgent
import shutil
import os

router = APIRouter()
agent = PersonalisedInterviewAgent()


@router.post('/upload')
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    upload_dir = os.path.join(os.path.dirname(__file__), '../../uploads')
    os.makedirs(upload_dir, exist_ok=True)
    dest = os.path.join(upload_dir, file.filename)
    with open(dest, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "path": dest}


@router.post('/analyze')
def analyze_resume(path: str):
    profile = agent.analyze_resume(path)
    return profile
