import streamlit as st
import sys
import os

# Ensure this frontend folder is on sys.path so local imports work when Streamlit runs the script
sys.path.insert(0, os.path.dirname(__file__))

from components.navbar import navbar
from pages import home, resume, interview_setup, interview, results

PAGES = {
    "Home": home,
    "Resume Upload": resume,
    "Interview Setup": interview_setup,
    "Interview": interview,
    "Results": results,
}


def main():
    st.set_page_config(page_title="Personalised Interview Preparation System", layout="wide")
    navbar()
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    with st.sidebar:
        st.title('Menu')
        page = st.radio('Navigation', list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state.page))
        st.session_state.page = page

    PAGES[st.session_state.page].app()


if __name__ == '__main__':
    main()
