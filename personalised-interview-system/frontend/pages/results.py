import streamlit as st
import requests
import os

API = os.getenv('API_BASE_URL','http://localhost:8000')


def app():
    st.header('Results')
    sid = st.session_state.get('session_id')
    if not sid:
        st.info('No session found')
        return
    r = requests.get(f"{API}/api/interview/{sid}/results")
    if r.ok:
        report = r.json()
        st.metric('Total Questions', report.get('total_questions'))
        st.metric('Correct', report.get('correct'))
        st.metric('Incorrect', report.get('incorrect'))
        st.metric('Average Score', report.get('average_score'))
        if st.button('Start New Interview'):
            st.session_state.page = 'Interview Setup'
    else:
        st.error('Failed to load results')
