import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di .env")

MODEL = "models/gemma-4-26b-a4b-it"

def normalize_text(text: str) -> str:
    """
    Internal preprocessing ONLY
    """
    if not text:
        return ""
    return text.strip()

def generate_gemma_response(prompt: str):
    client = genai.Client(api_key=API_KEY)
    cleaned = normalize_text(prompt)
    
    system_prompt = """
You are a multilingual speech-to-speech assistant.

TASK:
Generate natural, helpful responses based on user speech input.

INSTRUCTIONS:
- Do NOT change the meaning of the input
- Do NOT hallucinate or invent facts
- Answer naturally and conversationally
- Support Indonesian, English, and Arabic mixed input
- Use the same language style as the user when possible
- Keep responses concise (1-3 sentences)
- No markdown or special formatting

LANGUAGE RULES:
- If input is English → respond in English
- If input is Arabic → respond in Arabic
- If input is mixed → respond in Indonesian

DOMAIN RULES:
If the user asks about Umrah, Hajj, visa, hotel, transport, or travel:
- Give a direct answer first
- Provide practical steps or recommendations
- Do NOT ask follow-up questions unless absolutely necessary
- Be specific and actionable
"""
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=system_prompt + "\n\nUSER:\n" + cleaned
            )

            if response and response.text:
                return response.text.strip()

            return None

        except Exception as e:
                print(f"[GEMMA ERROR] attempt {attempt+1}: {e}")

                # kalau kena rate limit/quota
                if "quota" in str(e).lower() or "429" in str(e):
                    print("Rate limit hit. Sleep 60 sec...")
                    time.sleep(60)
                else:
                    time.sleep(3)

        return None