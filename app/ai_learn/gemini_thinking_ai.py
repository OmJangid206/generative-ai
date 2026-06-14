import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful assistant."
            "Before you explain, you first show that you are thinking by writing '🤔 Thinking...'."
            "Then give you answer"
         },
        {"role": "user", "content": "Explain to me how AI works"}
    ],
    reasoning_effort="low"
)


print(response.choices[0].message)