import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def get_math_answer(topic, question):
    if not api_key:
        return "❌ Error: OPENROUTER_API_KEY is not set."

    prompt = f"""
You are a highly accurate, step-by-step math tutor.

Topic: {topic}
Question: {question}

Instructions:
- Show clear, numbered steps
- Use exact values (fractions) where appropriate
- Handle symbolic math if topic is Linear Algebra, Algebra, or Calculus
- End with:
  ✅ Final Answer (exact): ...
  Approx: ...

If matrix-related, determine invertibility, steps to inverse if any.
Respond clearly:
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
        if "choices" not in json_data or not json_data["choices"]:
            return "❌ Error: Unexpected response format from tutor agent."

        return json_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as req_err:
        return f"❌ Request error: {req_err}"

    except Exception as err:
        return f"❌ Unexpected error: {err}"
