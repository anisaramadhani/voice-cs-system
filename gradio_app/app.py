import gradio as gr
import requests
import tempfile

API_URL = "http://127.0.0.1:8000/voice-chat"

def process(audio_path):

    if audio_path is None:
        return "", "", "", None

    with open(audio_path, "rb") as f:
        r = requests.post(
            API_URL,
            files={"audio": f}
        )

    stt = r.headers.get("X-STT", "")
    llm = r.headers.get("X-LLM", "")

    output_audio = None
    if r.content:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(r.content)
            output_audio = temp.name

    return stt, llm, output_audio


custom_css = """
.gradio-container {background: #f7fafd; border-radius: 18px; box-shadow: 0 4px 24px #0002;}
h1, .gr-markdown {color: #2d6cdf; font-weight: 700;}
.gr-button {background: linear-gradient(90deg, #2d6cdf 60%, #4ad9e2 100%) !important; color: #fff !important; border-radius: 10px !important; font-size: 1.1em;}
.gr-box, .gr-textbox, .gr-audio {border-radius: 12px !important; border: 1.5px solid #2d6cdf22 !important; background: #fff !important;}
.gr-textbox label, .gr-audio label {color: #2d6cdf; font-weight: 600;}
.gr-button:active {background: #4ad9e2 !important;}
.gr-markdown {font-size: 1.2em;}
#main-title {text-align: center !important; margin-bottom: 0.5em;}
"""

with gr.Blocks(title="Voice Chatbot") as demo:
    gr.Markdown("""
        # 🎙️ <span style='color:#2d6cdf'>Voice Chatbot</span>
        <div style='font-size:1.1em; color:#444; margin-bottom:16px;'>
        Upload audio, dapatkan transkripsi otomatis, respon LLM, dan output suara.
        </div>
    """, elem_id="main-title")

    audio = gr.Audio(type="filepath", label="🎵 Upload Audio", elem_id="audio-upload")
    btn = gr.Button("🚀 Jalankan", elem_id="run-btn")
    stt_box = gr.Textbox(label="1. Hasil Transkripsi STT Whisper", lines=3)
    llm_box = gr.Textbox(label="2. Respon LLM", lines=3)
    tts_audio = gr.Audio(label="3. Output Suara", elem_id="output-audio")

    btn.click(
        process,
        inputs=audio,
        outputs=[
            stt_box,
            llm_box,
            tts_audio
        ]
    )

demo.launch(css=custom_css)