import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate(system_prompt: str, user_prompt: str) -> str:
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content.strip()
