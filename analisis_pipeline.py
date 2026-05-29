import requests
import os
import time
import csv

API_URL = "http://127.0.0.1:8000/voice-chat"
AUDIO_DIR = "data/corpus/audio"
PROGRESS_FILE = "progress.txt"
RESULT_FILE = "hasil_analisis_pipeline.csv"

# =========================
# PROGRESS SYSTEM
# =========================
def get_progress():
    if not os.path.exists(PROGRESS_FILE):
        return set()

    with open(PROGRESS_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def add_progress(filename):
    with open(PROGRESS_FILE, "a") as f:
        f.write(filename + "\n")

# =========================
# SAVE RESULT CSV
# =========================
def append_result(row):
    file_exists = os.path.isfile(RESULT_FILE)

    with open(RESULT_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["file", "stt", "llm", "tts_audio", "latency"]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

# =========================
# MAIN PIPELINE
# =========================
def run_eval():
    files = sorted(
        [f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]
    )[:300]

    done_files = get_progress()

    print(f"Total file: {len(files)}")
    print(f"Already done: {len(done_files)}")

    for f in files:

        # =========================
        # SKIP YANG SUDAH SELESAI
        # =========================
        if f in done_files:
            print(f"SKIP: {f}")
            continue

        path = os.path.join(AUDIO_DIR, f)
        start = time.time()

        try:
            with open(path, "rb") as audio:

                files_payload = {"audio": audio}

                r = requests.post(
                    API_URL,
                    files=files_payload,
                    timeout=300
                )

            latency = round(time.time() - start, 3)

            # =========================
            # SUCCESS
            # =========================
            if r.status_code == 200:

                stt_text = r.headers.get("X-STT", "")
                llm_text = r.headers.get("X-LLM", "")

                output_audio_path = os.path.join(
                    "data",
                    "outputs",
                    f"tts_{f}"
                )
        
                row = {
                    "file": f,
                    "stt": stt_text,
                    "llm": llm_text,
                    "tts_audio": output_audio_path,
                    "latency": latency
                }

                append_result(row)
                add_progress(f)

                print(f"✓ SUCCESS: {f}")

            # =========================
            # ERROR API (TAPI LANJUT)
            # =========================
            else:
                print(f"✗ FAILED: {f} | status {r.status_code}")
                print(r.text)
                continue

        # =========================
        # ERROR NETWORK / TTS / DLL
        # =========================
        except Exception as e:
            print(f"✗ ERROR: {f} | {e}")
            continue

    print("\nDONE ALL FILES")

if __name__ == "__main__":
    run_eval()