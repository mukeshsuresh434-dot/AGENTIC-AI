import streamlit as st


def navbar():
    st.markdown("""
    <style>
    .header {background: linear-gradient(90deg,#4b6cb7,#182848); padding: 20px; color: white; border-radius:8px}
    </style>
    <div class='header'><h1>Personalised Interview Preparation System</h1><p>AI-powered interview practice</p></div>
    """, unsafe_allow_html=True)
