import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("LLM_PROVIDER", "gemini").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize GPT client if available
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def generate_response(prompt: str) -> str:
    """
    Routes to the selected LLM backend (Gemini 2.5 or GPT-4.1).
    """
    if provider == "gpt4" and openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ GPT-4.1 error: {e}"

    # Default: Gemini 2.5
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini error: {e}"
