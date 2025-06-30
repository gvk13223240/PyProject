# tutor_agent.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def get_math_answer(topic, question):
    if not api_key:
        return "❌ Error: OPENROUTER_API_KEY is not set."

    prompt = f"""
You are a highly accurate, patient, and step-by-step math tutor.

Topic: {topic}
Question: {question}

Instructions:
- Break the problem into logical steps
- Explain clearly without skipping steps
- Use exact math formatting where helpful
- End with: ✅ Final Answer: ...
"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        json_data = response.json()
        return json_data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"
