import os
import requests
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# download image
url = "https://images.pexels.com/photos/879109/pexels-photo-879109.jpeg"
img = requests.get(url).content

img64 = base64.b64encode(img).decode("utf-8")

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is this image?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64, {img64}"},
                },
            ],
        }
    ],
)

print(response.choices[0])
