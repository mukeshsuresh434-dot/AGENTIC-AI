import os
import requests

API = os.getenv('API_BASE_URL','http://localhost:8000')

def upload_resume(file_name: str, file_bytes: bytes):
    files = {'file': (file_name, file_bytes)}
    return requests.post(f"{API}/api/resume/upload", files=files)
