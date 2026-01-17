import os
from openai import OpenAI

# Groq OpenAI-compatible endpoint
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def generate(system_prompt: str, user_prompt: str) -> str:
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()
