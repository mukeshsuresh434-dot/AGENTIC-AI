import streamlit as st
import requests
import os

API = os.getenv('API_BASE_URL','http://localhost:8000')


def app():
    st.header('Interview Setup')
    interview_type = st.selectbox('Interview Type', ['aptitude','coding','technical','mixed'])
    difficulty = st.selectbox('Difficulty', ['easy','medium','hard','adaptive'], index=3)
    num = st.selectbox('Number of Questions', [5,10,15,20], index=1)

    if st.button('Start Interview'):
        # create session
        candidate_id = st.session_state.get('candidate_id', 1)
        payload = {
            'candidate_id': candidate_id,
            'interview_type': interview_type,
            'difficulty': difficulty,
            'total_questions': num
        }
        r = requests.post(f"{API}/api/interview/create", json=payload)
        if r.ok:
            sid = r.json().get('session_id')
            st.session_state.session_id = sid
            st.session_state.total_questions = num
            st.session_state.current_question = 0
            st.session_state.page = 'Interview'
        else:
            st.error('Failed to create interview session')
