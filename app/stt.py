import whisper
from app.utils import normalize_text

model = whisper.load_model("medium")

def transcribe_audio(path: str):
    result = model.transcribe(path)
    text = result["text"]
    return normalize_text(text)

