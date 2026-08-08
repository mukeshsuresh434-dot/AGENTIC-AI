import streamlit as st
import requests
import os

API = os.getenv('API_BASE_URL','http://localhost:8000')


def app():
    st.header('Interview')
    sid = st.session_state.get('session_id')
    if not sid:
        st.error('No active session. Go to setup.')
        return

    if 'question' not in st.session_state:
        # fetch first question
        r = requests.post(f"{API}/api/interview/{sid}/next-question")
        if r.ok:
            q = r.json()
            st.session_state.question = q
            st.session_state.current_question = st.session_state.get('current_question',0) + 1
        else:
            st.error('Failed to get question')
            return

    q = st.session_state.question
    st.subheader(f"Question {st.session_state.current_question} of {st.session_state.get('total_questions')}")
    st.write('Category:', q.get('category'))
    st.write('Difficulty:', q.get('difficulty'))
    st.markdown('**Question:**')
    st.write(q.get('question_text'))

    answer = st.text_area('Your Answer')
    if st.button('Submit Answer'):
        r = requests.post(f"{API}/api/interview/{sid}/submit", params={'question_id': q.get('question_id'), 'answer_text': answer})
        if r.ok:
            res = r.json()
            st.success(f"Score: {res.get('score')}")
            st.write('Feedback:', res.get('feedback'))
            st.write('Strengths:', res.get('strengths'))
            st.write('Weaknesses:', res.get('weaknesses'))
        else:
            st.error('Evaluation failed')

    if st.button('Next Question'):
        # fetch next question
        r = requests.post(f"{API}/api/interview/{sid}/next-question")
        if r.ok:
            q = r.json()
            st.session_state.question = q
            st.session_state.current_question += 1
            if st.session_state.current_question > st.session_state.get('total_questions', 0):
                st.session_state.page = 'Results'
        else:
            st.error('Failed to fetch next question')
