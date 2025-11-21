# Voice recognition
## Installation
### prepare OS
```sh
sudo apt update && sudo apt install ffmpeg 
```
### python packages
```sh
python3 -m venv virtual-env

source virtual-env/bin/activate
# pip install -U openai-whisper
```

## voice recognition
```python
import whisper

model = whisper.load_model("base") 
audio_file_path = "~/Downloads/1.mp3" # <-- Replace with your file path
language_code = "uk" # ISO 639-1 codes: "uk" - Ukrainian, "ru" - Russian

print(f"--- Transcribing audio file '{audio_file_path}' in language: {language_code}...")
result = model.transcribe(audio_file_path, language=language_code)  # language can be omitted: print("\nDetected Language:", result["language"])

print(f"--- Transcription Result, Language Forced: {result['language']}")
print(result["text"])
```