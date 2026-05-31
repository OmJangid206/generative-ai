import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter Client Configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ['OPEN_ROUTER_API']
)

# System Prompt for AI Chatbot
SYSTEM_PROMPT = """
    You are a helpful AI chatbot.
    Answer user questions clearly and simply.
"""

messages = [{
    "role":"system",
    "content": SYSTEM_PROMPT
}]

print(f"\n Chatbot started (type 'exit' to stop)\n")

# Choose Any Model
OPEN_AI_MODEL = "openai/gpt-4o-mini"
GEMINI_MODEL = "google/gemini-2.0-flash-001"
CLAUDE_MODEL = "anthropic/claude-3.5-sonnet"
GROQ_MODEL = "meta-llama/llama-3.3-70b-instruct"

while True:
    
    user_input = input("ask anything: ")
    
    if user_input.lower() == "exit":
        print("Chat ended.")
        break
    
    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get response from model
    response = client.chat.completions.create(
        model=OPEN_AI_MODEL,
        messages=messages
    )
    
    reply = response.choices[0].message.content
    print(f"Bot: {reply}\n")
    
    # Save bot reply for conversation memory
    messages.append({
        "role":"assistant",
        "content": reply
    })
