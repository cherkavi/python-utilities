import whisper
import sys
import os

model = whisper.load_model("base") 

if len(sys.argv) < 2:
    print("Error: Please provide the path to the audio file as a command-line argument.", file=sys.stderr)
    print("Usage: python mp3-transcript.py <path_to_audio_file>", file=sys.stderr)
    sys.exit(1)

audio_file_path = sys.argv[1]

if not os.path.exists(audio_file_path):
    print(f"Error: The file '{audio_file_path}' was not found.", file=sys.stderr)
    sys.exit(1)

language_code = "en" # ISO 639-1 codes: "uk" - Ukrainian, "ru" - Russian
result = model.transcribe(audio_file_path, language=language_code)  # language can be omitted: print("\nDetected Language:", result["language"])
print(result["text"])
