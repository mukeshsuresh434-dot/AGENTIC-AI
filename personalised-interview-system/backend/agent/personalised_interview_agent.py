from typing import Dict, Any, List, Optional
from backend.services import resume_parser, question_service, evaluation_service
from backend.services.llm_service import generate
from backend.database.database import SessionLocal
from backend.models.candidate import Candidate
from backend.models.interview import InterviewSession
from backend.models.question import Question
from backend.models.answer import Answer
import json


class PersonalisedInterviewAgent:
    def __init__(self):
        self.db = SessionLocal()

    def analyze_resume(self, path: str) -> Dict[str, Any]:
        parsed = resume_parser.parse_resume(path)
        profile = self.create_candidate_profile(parsed)
        return profile

    def create_candidate_profile(self, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        skills = parsed_resume.get('skills', [])
        projects = parsed_resume.get('projects', [])
        profile = {
            "skills": skills,
            "programming_languages": [s for s in skills if s.lower() in ('python','java','c++','c','javascript','sql')],
            "frameworks": [s for s in skills if s.lower() in ('react','django','flask','fastapi','streamlit')],
            "projects": projects,
            "experience": parsed_resume.get('text','')[:1000],
            "education": None,
            "target_role": "",
            "difficulty": 'medium',
        }
        return profile

    def save_candidate(self, profile: Dict[str, Any], resume_text: str, name: Optional[str]=None, email: Optional[str]=None, phone: Optional[str]=None) -> Candidate:
        c = Candidate(
            name=name,
            email=email,
            phone=phone,
            resume_text=resume_text,
            skills=json.dumps(profile.get('skills',[])),
            projects=json.dumps(profile.get('projects',[])),
            education=profile.get('education'),
            experience=profile.get('experience'),
        )
        self.db.add(c)
        self.db.commit()
        self.db.refresh(c)
        return c

    def create_interview_session(self, candidate_id: int, interview_type: str, difficulty: str, total_questions: int) -> InterviewSession:
        s = InterviewSession(
            candidate_id=candidate_id,
            interview_type=interview_type,
            difficulty=difficulty,
            total_questions=total_questions,
            current_question=0,
            status='in_progress'
        )
        self.db.add(s)
        self.db.commit()
        self.db.refresh(s)
        return s

    def generate_question(self, session: InterviewSession, candidate_profile: Dict[str,Any], previous_questions: List[str]=[]) -> Question:
        qdata = question_service.create_question(candidate_profile, session.interview_type, session.difficulty, previous_questions)
        q = Question(
            session_id=session.id,
            category=qdata.get('category'),
            question_text=qdata.get('question_text'),
            difficulty=qdata.get('difficulty'),
            topic=qdata.get('topic'),
            expected_answer=qdata.get('expected_answer')
        )
        self.db.add(q)
        session.current_question += 1
        self.db.add(session)
        self.db.commit()
        self.db.refresh(q)
        return q

    def evaluate_answer(self, question: Question, answer_text: str) -> Dict[str, Any]:
        res = evaluation_service.evaluate_answer({
            'expected_answer': question.expected_answer,
            'topic': question.topic
        }, answer_text)

        ans = Answer(
            question_id=question.id,
            answer_text=answer_text,
            score=res['score'],
            is_correct=res['is_correct'],
            feedback=res.get('feedback')
        )
        self.db.add(ans)
        self.db.commit()
        self.db.refresh(ans)
        return res

    def adapt_difficulty(self, session: InterviewSession, recent_score: int):
        # simple adaptation
        if session.difficulty == 'adaptive':
            # readjust difficulty string stored in session.difficulty var
            if recent_score >= 80:
                session.difficulty = 'hard'
            elif recent_score >= 50:
                session.difficulty = 'medium'
            else:
                session.difficulty = 'easy'
            self.db.add(session)
            self.db.commit()

    def identify_weak_areas(self, candidate_id: int):
        # placeholder: return topics with low avg score
        db = self.db
        # naive implementation
        return []

    def generate_final_report(self, session_id: int) -> Dict[str, Any]:
        # aggregate answers for session
        db = self.db
        session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
        questions = db.query(Question).filter(Question.session_id == session_id).all()
        answers = db.query(Answer).join(Question, Answer.question_id == Question.id).filter(Question.session_id == session_id).all()
        total = len(questions)
        correct = sum(1 for a in answers if a.is_correct)
        avg_score = int(sum(a.score for a in answers)/len(answers)) if answers else 0
        report = {
            'session_id': session_id,
            'total_questions': total,
            'correct': correct,
            'incorrect': total - correct,
            'average_score': avg_score,
        }
        return report
