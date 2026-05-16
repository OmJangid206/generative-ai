import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter Client Configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ['OPEN_ROUTER_API']
)

# Tool Function
def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city.strip().lower()}?format=%C+%t"

    try:
        response = requests.get(url, timeout=720)

        if response.status_code == 200:
            return f"The weather in {city.title()} is {response.text.strip()}"
        
        return f"Error: Server returned status code {response.status_code}"

    except Exception as err:
        return f"Error: {str(err)}"

# System Prompt for AI Agent
SYSTEM_PROMPT = """
    You are an AI Agent.

    You work in 4 steps:
    1. START
    2. PLAN
    3. TOOL (if needed)
    4. OUTPUT

    Rules:
    - Return only valid JSON
    - One step at a time
    - Follow the JSON format strictly
    - Do not explain outside JSON
    - Use TOOL only when required

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
    User: What is weather of Noida?
    {
        "step": "START",
        "content": "User is asking for weather of Noida"
    }
    {
        "step": "PLAN",
        "content": "The user wants current weather information"
    }
    {
        "step": "PLAN",
        "content": "I should use the get_weather tool"
    }
    {
        "step": "TOOL",
        "tool": "get_weather",
        "input": "Noida"
    }
    {
        "step": "OUTPUT",
        "content": "The weather in Noida is 30°C"
    }
"""

# Initial Message Setup
messages  = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# Take user input
user_query = input("Ask Anything: ")

messages.append(
    {
        "role": "user",
        "content": user_query
    }
)

# Agent Loop
while True:
    
    # Send conversation to model
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    
    # Extract model reply
    reply = response.choices[0].message.content
    print(f"\nAgent: {reply}")

    # Save assistant reply into history
    messages.append({
        "role": "assistant",
        "content": reply
    })
    
     # If model wants to use TOOL
    if '"step": "TOOL"' in reply:
        
        # Check which tool is requested
        if "get_weather" in reply:
            
            # Extract city name from JSON string
            city = reply.split('"input":')[1].split('"')[1]
            
            # Run actual Python tool
            result = get_weather(city)
            print(f"\nTool Result: {result}")
            
            # Send tool result back to model using OBSERVE pattern
            messages.append({
                "role": "user",
                "content": f"OBSERVE: {result}"
            })
        
    # Final Output Reached
    elif '"step": "OUTPUT"' in reply:
        
        # Convert JSON string - Python dict
        reply = json.loads(reply)
        
        # Print final clean answer
        print(f"\nFinal Answer")
        print(reply.get("content"))

        break
    
# ----------------------------
# print(response)
# ----------------------------
# Response 
# ChatCompletion(
#     id="gen-1778931216-nWr0qGmqheAHePegtE9d",
#     choices=[
#         Choice(
#             finish_reason="stop",
#             index=0,
#             logprobs=None,
#             message=ChatCompletionMessage(
#                 content='{\n    "step": "START",\n    "content": "User is asking for weather of Delhi"\n}',
#                 refusal=None,
#                 role="assistant",
#                 annotations=None,
#                 audio=None,
#                 function_call=None,
#                 tool_calls=None,
#                 reasoning=None,
#             ),
#             native_finish_reason="stop",
#         )
#     ],
#     created=1778931216,
#     model="openai/gpt-4o-mini",
#     object="chat.completion",
#     service_tier=None,
#     system_fingerprint="fp_eb37e061ec",
#     usage=CompletionUsage(
#         completion_tokens=23,
#         prompt_tokens=303,
#         total_tokens=326,
#         completion_tokens_details=CompletionTokensDetails(
#             accepted_prediction_tokens=None,
#             audio_tokens=0,
#             reasoning_tokens=0,
#             rejected_prediction_tokens=None,
#             image_tokens=0,
#         ),
#         prompt_tokens_details=PromptTokensDetails(
#             audio_tokens=0, cached_tokens=0, cache_write_tokens=0, video_tokens=0
#         ),
#         cost=5.925e-05,
#         is_byok=False,
#         cost_details={
#             "upstream_inference_cost": 5.925e-05,
#             "upstream_inference_prompt_cost": 4.545e-05,
#             "upstream_inference_completions_cost": 1.38e-05,
#         },
#     ),
#     provider="Azure",
# )