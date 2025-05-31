## download transcript
```python
# pip3 install --break-system-packages youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi

# https://www.youtube.com/watch?v=I51ay99999
video_id = 'I51ay99999'

ytt_api = YouTubeTranscriptApi()

# transcript_list = ytt_api.list(video_id)
transcript = ytt_api.fetch(video_id, languages=['ru', 'uk'])
print(
    transcript.video_id,
    transcript.language,
    transcript.language_code,
    transcript.is_generated
)

for snippet in transcript:
  print(snippet.text)
```
## download video
```python
# pip install pytube
from pytube import YouTube

def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


link = input("Enter the YouTube video URL: ")
Download(link)
```

