from fastapi import APIRouter, HTTPException
from backend.agent.personalised_interview_agent import PersonalisedInterviewAgent
from backend.schemas.interview import InterviewCreate

router = APIRouter()
agent = PersonalisedInterviewAgent()


@router.post('/create')
def create_interview(payload: InterviewCreate):
    s = agent.create_interview_session(payload.candidate_id, payload.interview_type, payload.difficulty, payload.total_questions)
    return {"session_id": s.id}


@router.post('/{session_id}/next-question')
def next_question(session_id: int):
    db = agent.db
    from backend.models.interview import InterviewSession
    from backend.models.candidate import Candidate
    from backend.models.question import Question as QuestionModel

    s = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")

    cand = db.query(Candidate).filter(Candidate.id == s.candidate_id).first()
    profile = {'skills': [], 'projects': []}
    try:
        import json
        if cand and cand.skills:
            profile['skills'] = json.loads(cand.skills)
        if cand and cand.projects:
            profile['projects'] = json.loads(cand.projects)
    except Exception:
        pass

    prev_qs = [q.question_text for q in db.query(QuestionModel).filter(QuestionModel.session_id == session_id).all()]

    q = agent.generate_question(s, profile, previous_questions=prev_qs)
    return {
        "question_id": q.id,
        "category": q.category,
        "question_text": q.question_text,
        "difficulty": q.difficulty,
        "topic": q.topic,
    }


@router.post('/{session_id}/submit')
def submit_answer(session_id: int, question_id: int, answer_text: str):
    db = agent.db
    from backend.models.question import Question as QuestionModel
    from backend.models.interview import InterviewSession

    q = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail='Question not found')
    res = agent.evaluate_answer(q, answer_text)
    s = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if s:
        agent.adapt_difficulty(s, res.get('score', 0))
    return res


@router.get('/{session_id}/results')
def get_results(session_id: int):
    report = agent.generate_final_report(session_id)
    return report
