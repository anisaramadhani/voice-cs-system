from gtts import gTTS
from pydub import AudioSegment
import os
import tempfile
import re

OUTPUT_DIR = "data/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text: str):
    if not text:
        return "id"

    text = text.lower()

    # 1. Arabic check
    if re.search(r"[\u0600-\u06FF]", text):
        return "ar"

    # 2. English keyword scoring
    english_markers = [
        " i ", " you ", " we ", " they ",
        " is ", " are ", " the ",
        " to ", " and ", " of ", " in "
    ]

    score = sum(1 for marker in english_markers if marker in f" {text} ")

    if score >= 3:
        return "en"

    # default
    return "id"

# =========================
# TEXT TO SPEECH
# =========================
def text_to_speech(text: str, output_path: str):
    if not text:
        text = "empty response"

    try:
        lang = detect_language(text)

        if lang == "ar":
            tts_lang = "en"
        else:
            tts_lang = lang

        print(f"[TTS DEBUG] detected language: {lang}")

        temp_mp3 = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ).name

        # generate TTS
        tts = gTTS(
            text=text,
            lang=tts_lang,
            slow=False
        )

        tts.save(temp_mp3)

        # convert mp3 -> wav
        sound = AudioSegment.from_mp3(temp_mp3)
        sound.export(output_path, format="wav")

        # hapus temp file
        os.remove(temp_mp3)

        print(f"[TTS] success | lang={tts_lang} -> {output_path}")

        return output_path

    except Exception as e:
        print("[TTS ERROR]", e)
        raise e