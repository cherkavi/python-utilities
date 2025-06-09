# pip3 install --break-system-packages youtube-transcript-api
# python3

from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re

if len(sys.argv) < 2:
    print("link to youtube video (example: https://www.youtube.com/watch?v=aGwb1KLmtog) should be provided as first argument", file=sys.stderr)
    sys.exit(1)
youtube_url:str = sys.argv[1]

if len(sys.argv) > 2:
    video_languages = sys.argv[2:] 
else:
    video_languages=['en']


def get_youtube_video_id(url):
    # Regular expression to match the YouTube video ID
    match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

video_id = get_youtube_video_id(youtube_url)
# video_id='dQw4w9WgXcQ'

ytt_api = YouTubeTranscriptApi()
# transcript_list = ytt_api.list_transcripts(video_id)
# transcript_list.find_transcript(['en']).fetch()
# transcript_en = ytt_api.list(video_id).find_transcript(['en'])
# dir(transcript_list)
# transcript_en.fetch()

transcript = ytt_api.fetch(video_id, languages=video_languages)
print(
    transcript.video_id,
    transcript.language,
    transcript.language_code,
    transcript.is_generated
)

for snippet in transcript:
  print(snippet.text)
