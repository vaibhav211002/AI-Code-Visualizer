import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def explain_code(source_code: str) -> dict:
    prompt = f"""
You are a code explainer. Analyze the following code and return a JSON object with exactly these keys:
- "explanation": simple English explanation for someone new to programming
- "complexity": time complexity like O(n), O(n^2) etc with a one line reason

Return only valid JSON, no markdown, no extra text.

Code:
{source_code}
"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
            },
            timeout=30.0
        )

    result = response.json()
    if "choices" not in result:
        print("Groq API error:", result)  # this will show in terminal
        return {
            "explanation": result.get("error", {}).get("message", "AI explanation failed"),
            "complexity": "N/A"
        }

    raw = result["choices"][0]["message"]["content"]

    import json
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "explanation": raw,
            "complexity": "Could not parse complexity"
        }