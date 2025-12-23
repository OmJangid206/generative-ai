import requests
from pydantic import BaseModel, Field
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    
    return "Something went wrong"

avaialble_tool = {
    "get_weather": get_weather
}

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

class OutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, ete")
    content: Optional[str] = Field(..., description="The optional string content for the step")
    tool: Optional[str] = Field(..., description="The ID of the tool to call.")
    input: Optional[str] = Field(..., description="The input params for the tool")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("Enter your query:")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model="gpt-4o",
            response_format=OutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result })

        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = avaialble_tool[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input})")
            message_history.append({"role": "developer", "content": json.dumps(
                { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response }
            )})
            continue

        if parsed_result.step == "PLAN":
            print("PLAN", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("OUTPUT", parsed_result.content)
            break

    print("\n\n\n")