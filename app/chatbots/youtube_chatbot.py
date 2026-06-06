# pip install youtube-transcript-api
# pip install yt-dlp
# pip install openai-whisper

import os
import yt_dlp
import whisper
import glob
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Load Env
load_dotenv()

# OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

# Model config
MODEL = "openai/gpt-4o-mini"


def transcript_video(url):
    """
    Get transcript from YouTube captions.
    If captions are unavailable, use Whisper.
    """
    try:
        print("Fetching YouTube transcript...")
        return get_youtube_transcript(url)

    except Exception as e:
        print(f"Transcript API failed: {str(e)}")
        print("Using Whisper fallback")
        return whisper_transcribe(url)

    
def get_youtube_transcript(url):
    
    # Extract Video ID
    parsed_url = urlparse(url)
    print(f"parsed_url: {parsed_url}")

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        video_id = parse_qs(parsed_url.query)["v"][0]
        print(f"video_id: {video_id}")
        
    elif parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path[1:]
        print(f"video_id1: {video_id}")

    else:
        raise ValueError("Invalid Youtube URL")
    
    # Fetch transcript
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    # transcript = transcript_list.find_transcript(["en-US", "en"])
    transcript = next(iter(transcript_list))
    transcript = transcript.fetch()
    # transcript = api.fetch(video_id)

    # Convert transcript list to single text
    text = " ".join(item.text for item in transcript)
    # text = " ".join(snippet.text for snippet in transcript.snippets) # Same response
    print(f"text: {text}")

    return text


def download_audio(url):
    
    # Delete old audio file if any
    for file in glob.glob("audio.*"):
        os.remove(file)
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "quiet": True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    files = glob.glob("audio.*")
    print(f"files: {files}")

    if not files:
        raise FileNotFoundError("Audio download failed")
    
    return files[0]


def  whisper_transcribe(url):

    print("Downloading audio...")
    audio_file = download_audio(url)

    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Starting transcription...")
    result = model.transcribe(audio_file)

    print("Transcription completed.")

    return result["text"]
 
# -----------------------------
# Youtube URL
URL = input("Enter Youtube URL: ")
transcript = transcript_video(URL)

# System Prompt
SYSTEM_PROMPT = f"""
You are a youtube Assistant.
Answer questions ONLY using the youtube content below.
If the answer not find from the youtube content:
say: 'Could not find information Please ask youtube content related data.'

YOUTUBE CONTENT: {transcript[:10000]}
"""

messages = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]

print("Youtube Chatbot started.")

while True:
    
    user_query = input("Ask youtube content related anything: ")
    
    if user_query.lower() == "exit":
        print("Chat bot stoped.")
        break

    messages.append({
        "role": "user",
        "content": user_query
    })
    
    response = client.chat.completions.create(
        model=MODEL, messages=messages
    )
    
    answer = response.choices[0].message.content
    
    print("\nBot: ", answer)
    print()
    
    messages.append({
        "role": "assistant",
        "content": answer
    })
    