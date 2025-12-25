# Voice recognition
## Installation
### prepare OS

For GPU support, you will need to install the NVIDIA CUDA Toolkit.

```sh
sudo apt update && sudo apt install ffmpeg 
```
### installation
```sh
python3 -m venv virtual-env; source virtual-env/bin/activate
# pip3 install -U openai-whisper
sudo apt install python3-openai-whisper
```

## usage
### usage bash
```sh
whisper "1.mp3" --model base --output_format srt
```

### usage python
```python
import whisper

## https://github.com/openai/whisper#avialable-models-and-languages
# tiny, base, small, medium, large-v1, large-v2, large-v3
# tiny.en, base.en, small.en, medium.en
model = whisper.load_model("base") 
audio_file_path = "~/Downloads/1.mp3" # <-- Replace with your file path
language_code = "uk" # ISO 639-1 codes: "uk" - Ukrainian, "ru" - Russian

print(f"--- Transcribing audio file '{audio_file_path}' in language: {language_code}...")
result = model.transcribe(audio_file_path, language=language_code)  # language can be omitted: print("\nDetected Language:", result["language"])

print(f"--- Transcription Result, Language Forced: {result['language']}")
print(result["text"])
```