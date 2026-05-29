import os
import re

def normalize_text(text):
    if not text:
        return ""

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[*_/]", "", text)

    return text

def ensure_temp():
    os.makedirs("data/temp", exist_ok=True)