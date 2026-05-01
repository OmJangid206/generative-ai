# pip install openai requests python-dotenv
# https://openrouter.ai/docs/quickstart

import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Open Router Config
client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=os.environ['OPEN_ROUTER_API']
)

# Tool function
def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Somwthing went wrong"

# System Prompt
SYSTEM_PROMPT = """
You are an AI Agent.

You work in 3 steps:
1. START
2. PLAN
3. OUTPUT

You can also use TOOL if needed.

Rules:
- Return only JSON
- One step at a time
- Follow this format strictly

JSON Format:
{
  "step": "START" | "PLAN" | "TOOL" | "OUTPUT",
  "content": "string",
  "tool": "string",
  "input": "string"
}

Available Tools:
- get_weather(city: str)

Example:
User: What is weather of Delhi?

{
  "step": "PLAN",
  "content": "User is asking for weather information"
}

{
  "step": "PLAN",
  "content": "We should use get_weather tool"
}

{
  "step": "TOOL",
  "tool": "get_weather",
  "input": "Delhi"
}
"""

# Main App
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input("Ask Something: ")
messages.append({
    "role": "user",
    "content": query
})

while True:
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    print(f"\nAgent Reply: {reply}")
    
    messages.append({
        "role": "assistant",
        "content": reply
    })
    
    # Tool Handling
    if '"step": "TOOL"' in reply:
        if "get_weather" in reply:
            city = reply.split('"input":')[1].split('"')[1]
            
            tool_result = get_weather(city)
            print("\nTool Result:", tool_result)
            
            messages.append({
                "role": "user",
                "content": f"OBSERVE: {tool_result}"
            })
    elif '"step": "OUTPUT"' in reply:
        print("\nFinal Answer Reached")
        break