import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

MODEL = "google/gemini-2.0-flash-001"

MEMORY_FILE = 'chat_memory.json'

SYSTEM_PROMPT = """
You are an AI assistant.

Rules:
- Remember perious conversation
- Answer clearly
- Keep context of chat
"""

# Load Memory
def load_memory():
    
    if os.path.exists(MEMORY_FILE):
        
        with open(MEMORY_FILE, 'r') as file:
            content = file.read().strip()
            if content:
                return json.load(file)
    return [{
        'role': 'system',
        'content': SYSTEM_PROMPT
    }]
    
# Save Memory
def save_memory(messages):
    
    with open(MEMORY_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

# Load Previous Messages
messages = load_memory()

print("\n Memory Chatbot Started")

while True:
    
    user_input = input('Ask anything? ')
    
    # Exit
    if user_input.lower() == "exit":
        print("Chat ended.")
        break
    
    # Reset Memory
    if user_input.lower() == "reset":

        messages = [{
            'role': 'system',
            'content': SYSTEM_PROMPT
        }]
        save_memory(messages)
        print('\nMemory cleared')

    # Add User Message
    messages.append({
        'role': 'user',
        'content': user_input
    })
    
    try:
        # Streaming Response
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        print("\nBot: ", end="")
        full_reply = ""
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                
                full_reply += text
                print(text, end="", flush=True)

        print("\n")
        
        # Save Assistant Reply
        messages.append({
            "role": "assistant",
            "content": full_reply
        })
        
        # Save Memory to File
        save_memory(messages)
        
        
    except Exception as e:
        print(f"\nError: {e}\n")
    
    
    