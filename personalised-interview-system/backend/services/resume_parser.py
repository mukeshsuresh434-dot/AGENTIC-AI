import os
import re
from typing import Dict, List

import docx
from PyPDF2 import PdfReader


def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    out = []
    for p in reader.pages:
        out.append(p.extract_text() or "")
    return "\n".join(out)


def parse_resume(path: str) -> Dict:
    text = ""
    if path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(path)
    elif path.lower().endswith(".docx"):
        text = extract_text_from_docx(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    # simple extractions
    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.search(r"\+?\d[\d\-\s]{7,}\d", text)

    skills = []
    projects = []

    # heuristics: look for sections
    sections = re.split(r"\n{2,}", text)
    for s in sections:
        low = s.lower()
        if "skill" in low or "techn" in low:
            parts = re.split(r"[:,\n]", s)
            for p in parts:
                if len(p.strip()) > 2 and len(skills) < 50:
                    skills.extend([x.strip() for x in p.split(",") if x.strip()])
        if "project" in low:
            lines = [l.strip() for l in s.splitlines() if l.strip()]
            projects.extend(lines[:5])

    # dedupe and filter
    skills = list(dict.fromkeys([s for s in skills if len(s) < 50]))[:50]
    projects = list(dict.fromkeys(projects))[:10]

    return {
        "text": text,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "skills": skills,
        "projects": projects,
    }
