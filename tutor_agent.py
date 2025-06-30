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
- Solve the system using Gauss-Jordan Elimination
- Use exact values (fractions) where possible
- Do not guess or skip steps
- Clearly write all intermediate steps
- At the end, return both the exact solution (fractions) and decimal approximations
- End with: ✅ Final Answer: ...

Example format:
x = ..., y = ..., z = ... (exact)
x ≈ ..., y ≈ ..., z ≈ ... (approximate)
"""

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

        # Defensive check for unexpected API structure
        if "choices" not in json_data or not json_data["choices"]:
            print("⚠️ Unexpected response structure:", json_data)
            return "❌ Error: Unexpected response format from tutor agent."

        return json_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as req_err:
        print("❌ Request failed:", req_err)
        return "❌ Error: Could not connect to the tutor service."

    except Exception as err:
        print("❌ Unexpected error:", err)
        return "❌ Error: An unexpected error occurred in the tutor agent."
