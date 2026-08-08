from typing import Dict, Any
import random
from backend.services.llm_service import generate


def create_question(candidate_profile: Dict[str, Any], interview_type: str, difficulty: str, previous_questions: list) -> Dict:
    # create a dynamic prompt
    topics = candidate_profile.get("skills", [])[:5] or ["programming"]
    topic = random.choice(topics)
    category = interview_type if interview_type != 'mixed' else random.choice(['aptitude','coding','technical','resume'])

    prompt = f"Generate a {difficulty} {category} question about {topic} for a candidate with skills {candidate_profile.get('skills')}."
    prompt += "\nProvide expected_answer and topic in JSON format."

    text = generate(prompt, max_tokens=250)

    # naive parsing: return generated text as question_text and expected_answer
    q = {
        "category": category,
        "question_text": text.split('\n')[0] if text else f"Explain {topic}",
        "difficulty": difficulty,
        "topic": topic,
        "expected_answer": '\n'.join(text.split('\n')[1:])[:1000] if text else "",
    }
    return q
