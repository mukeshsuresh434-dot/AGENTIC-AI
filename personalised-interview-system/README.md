# Personalised Interview Preparation System

AI-powered interview practice platform using Streamlit frontend and FastAPI backend.

## Quickstart

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` if available.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Start backend:

```
uvicorn backend.main:app --reload
```

4. Start frontend:

```
streamlit run frontend/app.py
```

The system uses SQLite at `backend/data/interview.db`.
