from faster_whisper import WhisperModel
import os

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"{audio_path} not found.")

    segments, _ = model.transcribe(audio_path)
    full_text = " ".join([seg.text for seg in segments])
    return full_text.strip()