import os
from PIL import Image
from io import BytesIO
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

response = client.images.generate(
    model="imagen-3.0-generate-002",
    prompt="a portrait of a sheepadoodle wearing a cape",
    response_format="b64_json",
    n=1
)

for image_data in response.data:
    image = Image.open(BytesIO(base64.b64decode(image_data.b64_json)))
    image.show()