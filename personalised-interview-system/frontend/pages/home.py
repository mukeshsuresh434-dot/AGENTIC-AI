import streamlit as st


def app():
    st.title('Personalised Interview Preparation System')
    st.subheader('AI-powered interview preparation based on your resume.')
    st.write('- Resume-based questions')
    st.write('- Aptitude practice')
    st.write('- Coding practice')
    st.write('- Technical interview')
    st.write('- Adaptive difficulty')
    st.write('- AI feedback')

    if st.button('Start Preparation'):
        st.session_state.page = 'Resume Upload'
