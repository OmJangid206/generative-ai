# pip install google-genai

import os
from google import genai
from dotenv import load_dotenv
 
load_dotenv()

client = genai.Client(
    api_key=os.environ['GEMINI_API_KEY']
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI work in a few words",
)

# print(response)
# print(response.parts)
print(response.text)
# print(response.response_id)
