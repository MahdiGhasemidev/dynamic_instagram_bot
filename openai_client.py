from openai import OpenAI
import os

# Load API key از Environment variable
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise Exception("❌ Set OPENAI_API_KEY environment variable.")

# ساخت client با base_url سفارشی
client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key=API_KEY
)

DEFAULT_MODEL = "gpt-4o"


def chat_completion(prompt, model=DEFAULT_MODEL):
    """
    Generate text using GapGPT API in the style of OpenAI client.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ GapGPT API Error:", e)
        return None