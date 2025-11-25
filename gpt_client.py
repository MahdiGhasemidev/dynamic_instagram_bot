import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("❌ Set OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_completion(prompt, model="gpt-4.1-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("❌ OpenAI API Error:", e)
        return None