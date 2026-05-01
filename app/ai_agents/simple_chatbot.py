import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API")
)

print("AI Chatbot")


while True:
    
    user_input = input("AI Chatbot Started! Type 'exit' to quit.\n")
    
    if user_input.lower() == 'exit':
        print("Bot: Good bye")
        break

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system","content": "You are helpfull AI Assistant"},
                {
                "role": "user",
                'content': user_input 
                }
            ]
        )
        
        reply = response.choices[0].message.content
        print(f"Bot: {reply}")
    except Exception as e:
        print("Error:", str(e))