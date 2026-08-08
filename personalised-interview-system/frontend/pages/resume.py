import streamlit as st
import requests
import os

API = os.getenv('API_BASE_URL','http://localhost:8000')


def app():
    st.header('Upload your Resume')
    uploaded = st.file_uploader('Upload PDF or DOCX', type=['pdf','docx'])
    if uploaded:
        st.write('File:', uploaded.name)
        if st.button('Analyze Resume'):
            files = {'file': (uploaded.name, uploaded.getvalue())}
            with st.spinner('Analyzing your resume...'):
                r = requests.post(f"{API}/api/resume/upload", files=files)
                if r.ok:
                    data = r.json()
                    path = data['path']
                    r2 = requests.post(f"{API}/api/resume/analyze", params={'path': path})
                    if r2.ok:
                        profile = r2.json()
                        st.session_state.candidate_profile = profile
                        st.session_state.resume_path = path
                        st.success('Analysis complete')
                        st.session_state.page = 'Interview Setup'
                    else:
                        st.error('Analysis failed')
                else:
                    st.error('Upload failed')

    if 'candidate_profile' in st.session_state:
        st.subheader('Candidate Profile')
        p = st.session_state.candidate_profile
        st.write('Skills:', p.get('skills'))
        st.write('Projects:', p.get('projects'))
        if st.button('Save & Proceed'):
            st.session_state.page = 'Interview Setup'
