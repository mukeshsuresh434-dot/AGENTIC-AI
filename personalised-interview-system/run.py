"""Run helpers for dev"""
import os
import subprocess

def run_backend():
    subprocess.run(["uvicorn", "backend.main:app", "--reload"])

def run_frontend():
    subprocess.run(["streamlit", "run", "frontend/app.py"])

if __name__ == '__main__':
    print("Use run_backend() or run_frontend()")