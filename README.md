# Multilingual Code-Switching Voice Chatbot – Whisper, Gemma LLM, gTTS Integration

Proyek ini merupakan aplikasi chatbot speech-to-speech multilingual yang mampu menangani input suara dengan code-switching antara Bahasa Indonesia, Inggris, dan Arab. Sistem akan mentranskripsi suara (Speech-to-Text), memahami konteks menggunakan Large Language Model (Gemma via Google GenAI SDK), lalu menghasilkan respons suara (Text-to-Speech).

## 📌 Fitur Utama
- 🎙️ Speech-to-Text (STT) menggunakan OpenAI Whisper.
- 🧠 LLM Integration menggunakan Google Gemma 4 26B untuk respons kontekstual multilingual.
- 🔊 Text-to-Speech (TTS) menggunakan Google Text-to-Speech (gTTS).
- 🌐 Antarmuka pengguna interaktif berbasis Gradio dan backend FastAPI.
- 🧪 Script analisis otomatis dataset dan evaluasi hasil ke CSV.

## 🗂️ Struktur Proyek
```
voice-cs-system/
│
├── app/
│   ├── main.py            # Endpoint utama FastAPI
│   ├── llm.py             # Integrasi Gemma LLM
│   ├── stt.py             # Transkripsi suara (Whisper)
│   ├── tts.py             # TTS dengan gTTS
│   ├── utils.py           # Utility functions
│   └── __init__.py
│
├── gradio_app/
│   └── app.py             # Frontend dengan Gradio
│
├── data/
│   ├── corpus/            # Dataset audio
│   ├── outputs/           # Output audio hasil sistem
│   └── temp/              # File sementara
│
├── analisis_pipeline.py   # Script analisis otomatis dataset
├── hasil_analisis_pipeline.csv # Hasil evaluasi otomatis
├── requirements.txt       # Daftar dependensi Python
├── progress.txt           # Daftar file audio yang sudah diproses (tracking progress dataset)
├── env/                   # Virtual environment (jika ada)
```

## 📚 Catatan
- Semua file audio menggunakan format `.wav`.
- Sistem mendukung code-switching Bahasa Indonesia, Inggris, dan Arab.
- Model Whisper yang direkomendasikan: `large-v3`.
- LLM: Google Gemma 4 26B via GenAI SDK.
- TTS: Google Text-to-Speech (gTTS) default.
- Script analisis otomatis dapat digunakan untuk evaluasi batch dataset.

## 👨‍💻 Dibuat Untuk
Proyek UAS praktikum *Pemrosesan Bahasa Alami*

---

> Oleh: Anisa Ramadhani (2308107010008) — Informatika, Universitas Syiah Kuala
