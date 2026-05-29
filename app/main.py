import os
import uuid
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse

from app.stt import transcribe_audio
from app.llm import generate_gemma_response   
from app.tts import text_to_speech

app = FastAPI()

TEMP_DIR = "data/temp"
OUTPUT_DIR = "data/outputs"
CSV_PATH = "hasil_analisis_pipeline.csv"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================
# CSV SAFE LOOKUP
# ======================
def get_from_csv(filename: str):
    if not os.path.exists(CSV_PATH):
        return None

    df = pd.read_csv(CSV_PATH)

    # safety normalize
    df["file"] = df["file"].astype(str).str.strip().str.lower()
    filename = filename.strip().lower()

    match = df[df["file"] == filename]

    if match.empty:
        return None

    return str(match.iloc[0]["llm"])


@app.post("/voice-chat")
async def voice_chat(
    audio: UploadFile = File(...)):

    print("[DEBUG] filename:", audio.filename)

    if not audio.filename.endswith(".wav"):
        return JSONResponse({"error": "Only WAV allowed"}, status_code=400)

    input_path = os.path.join(TEMP_DIR, audio.filename)
    output_path = os.path.join(
        OUTPUT_DIR,
        f"tts_{audio.filename}"
    )

    try:
        # SAVE AUDIO
        with open(input_path, "wb") as f:
            f.write(await audio.read())

        # STT
        text = transcribe_audio(input_path)

        # GEMMA LLM
        response = generate_gemma_response(text)

        # ERROR CHECK
        if (
            response is None
            or len(str(response).strip()) == 0
            or "quota" in str(response).lower()
            or "exceeded" in str(response).lower()
        ):

            return JSONResponse(
            {
                "error": "LLM gagal memproses request",
                "file": audio.filename,
                "stt": text
            },
            status_code=503
        )

        # TTS
        text_to_speech(response, output_path)

        return FileResponse(
            output_path,
            media_type="audio/wav",
            headers={
                "X-STT": text,
                "X-LLM": response
            }
        )

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)