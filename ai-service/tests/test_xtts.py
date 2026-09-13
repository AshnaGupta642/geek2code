from TTS.api import TTS

print("Loading model... this may take a few minutes the first time (downloading ~2GB).")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
print("Model loaded successfully!")