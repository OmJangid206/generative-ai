from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

resp = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Explain how the human mind works in one line"}
    ]
)

# print(resp)
# print(resp.choices[0])
# print(resp.choices[0].message)
print(resp.choices[0].message.content)
