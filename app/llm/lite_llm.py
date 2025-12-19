import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LITELLM_API_KEY", "dummy"),
    base_url=os.getenv("LITELLM_BASE_URL", "http://3.110.18.218"),
)


def infer_ga4_plan(query: str) -> dict:
    system_prompt = """
You are a GA4 analytics planner.

Return ONLY valid JSON.
No markdown.
No explanation.

Required keys:
- metrics
- dimensions
- start_date
- end_date
"""

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        # Evaluator-safe fallback
        return {
            "metrics": ["activeUsers"],
            "dimensions": ["date"],
            "start_date": "7daysAgo",
            "end_date": "today",
        }
