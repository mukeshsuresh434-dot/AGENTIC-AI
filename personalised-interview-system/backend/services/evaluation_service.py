from typing import Dict
import random


def evaluate_answer(question: Dict, answer_text: str) -> Dict:
    # Simple heuristic evaluation: length and overlap
    score = 0
    expected = (question.get('expected_answer') or '').lower()
    at = (answer_text or '').lower()
    if not at.strip():
        return {"score": 0, "is_correct": False, "feedback": "No answer provided."}

    # reward length
    score += min(40, len(at.split()) )
    # reward keyword overlap
    for w in expected.split()[:20]:
        if w in at:
            score += 1

    score = min(100, int(score))
    is_correct = score >= 50
    feedback = "Good answer." if is_correct else "Needs improvement. Focus on core concepts and examples."
    # simple strengths/weaknesses
    strengths = []
    weaknesses = []
    if is_correct:
        strengths.append(question.get('topic'))
    else:
        weaknesses.append(question.get('topic'))

    return {
        "score": score,
        "is_correct": is_correct,
        "feedback": feedback,
        "strengths": strengths,
        "weaknesses": weaknesses,
    }
