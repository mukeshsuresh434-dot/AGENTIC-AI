import os
import json
import random

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate(prompt: str, max_tokens: int = 200) -> str:
    """Generate text using OpenAI if key present, otherwise use a simple fallback."""
    if OPENAI_API_KEY:
        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    # Fallback simple generator
    snippets = [
        "Explain the concept and give an example.",
        "Describe steps and best practices.",
        "List 3 common pitfalls and how to avoid them.",
    ]
    return random.choice(snippets) + "\n\n" + prompt[:max_tokens]
