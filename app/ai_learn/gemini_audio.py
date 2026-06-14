import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

with open("/home/moglix/Desktop/moglix/learning/generative-ai/app/ringtone-021-365652.mp3", "rb") as audio_file:
    base64_audio = base64.b64encode(audio_file.read()).decode("utf-8")

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Transcribe this audio",
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": base64_audio,
                        "format": "mp3"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)