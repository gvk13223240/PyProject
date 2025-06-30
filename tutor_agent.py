import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def get_math_answer(topic, question):
    prompt = f"""
You are a highly accurate, patient, and step-by-step math tutor.

Topic: {topic}
Question: {question}

Instructions:
- Break down the solution into logical, numbered steps
- Explain each step clearly
- Use simple math formatting
- Do not skip steps
- End with: ✅ Final Answer: ...

Respond clearly:
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # You can change model here
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
