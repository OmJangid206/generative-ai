import os
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

# export GOOGLE_APPLICATION_CREDENTIALS="/home/moglix/Desktop/moglix/Personal-Project/generative-ai/app/service_account.json"
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/omprakashjangid/Desktop/Personal-Project/generative-ai/app/service_account.json"

# ---------------- CONFIG ----------------
PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"

client = genai.Client(
    vertexai=True, 
    project= PROJECT_ID, 
    location=LOCATION
)

SYSTEM_PROMPT = """
    You're are expert in AI Assistant in resolving user queries using chain of thought.
    You work on START,PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think the PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at the time.
    - The sequence of steps is START(where user gives an input), PLAN(That can be multiple time) and OUTPUT(This the the final output which is going to be dispplayed to uses).

    Output JSON Format:
    { "step": "START" | "PLAN" | "STOP" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Avaialble Tools:
    - get_weather(city: str): Takes city name as input and return the weather info as output. 

    Example:
    START: What is weather of Delhi?
    PLAN: { "step": "PLAN": "content": "seems like user is intrested in weather of Delhi in india." }
    PLAN: { "step": "PLAN": "content": "let's see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "We have avaialble tool get_weather we need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE", "tool": "get_weather", "output": "The temp of the delhi is 20 C cloudy" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather of delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The current weather in the delhi is 33 C with some cloudy sky. " }
"""
print("\n\n\n")

def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    
    return "Something went wrong"


available_tool = {
    "get_weather": get_weather
}

class OutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, ete")
    content: Optional[str] = Field(..., description="The optional string content for the step")
    tool: Optional[str] = Field(..., description="The ID of the tool to call.")
    input: Optional[str] = Field(..., description="The input params for the tool")


message_history = []

while True:
    user_query = input("Enter your query: ")
    message_history.append(user_query)

    while True:
        prompt = SYSTEM_PROMPT + "\n" + "\n".join(message_history)
        # print("-----------------")
        # print(f"prompt: {prompt}")
        # print("-----------------")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=OutputFormat,
            ),
        )

        raw_text = response.text.strip()
        print("---------------------------")
        print(raw_text)
        print("---------------------------")
        try:
            parsed = OutputFormat(**json.loads(raw_text))
        except Exception:
            print("Invalid JSON from model")
            print(raw_text)
            break

        message_history.append(raw_text)

        if parsed.step == "START":
            print("START:", parsed.content)

        elif parsed.step == "PLAN":
            print("PLAN:", parsed.content)

        elif parsed.step == "TOOL":
            tool_output = available_tool[parsed.tool](parsed.input)
            observe = json.dumps({
                "step": "OBSERVE",
                "tool": parsed.tool,
                "input": parsed.input,
                "output": tool_output
            })
            message_history.append(observe)

        elif parsed.step == "OUTPUT":
            print("OUTPUT:", parsed.content)
            break

    print("\n----------------------\n")
