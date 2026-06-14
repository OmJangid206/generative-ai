import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is  {response.text}"
    return "Something went wrong"

available_tools= {
    "get_weather": get_weather,
}

SYSTEM_PROMPT = """
    You are an export AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give the OUTPUT.
    You can also call a tool if required  from the list of available tools.
    For every tool call wait for the observe step which is the output for the called tool.

    Rules:
    - Strictly follow the given json output format
    - Only run one step at the time.
    - The Sequence of the step is START (Where user gives the input), PLAN (That can be multiple times) and finally the OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools: 
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city.

    Example 1: 
    START: What is weathe of Mumbai?
    PLAN: {"step": "PLAN": "content": "Seems like  user is interested in getting weather of Delhi in India" }
    PLAN: {"step": "PLAN": "content": "Let's see if we have available tool from the list of avaialble tools" }
    PLAN: {"step": "PLAN": "content": "Great, we have get_weather tool available tool for this query." }
    TOOL: {"step": "TOOL": "get_weather", "input": "mumbai" }
    PLAN: {"step": "OBSERVE": "tool": "get_weather", "output": "The temp of the mumbai is cloudy with 20.C" }
    PLAN: {"step": "PLAN": "content": "Great, I got the weather info about delhi" }
    OUTPUT: {"step": "OUTPUT", "content": "The cuurent weather in delhi is 20 C with some cloudy sky."}
"""

print("\n\n\n")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]


while True:
    user_query = input("👉🏻 ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=message_history
        )

        raw_result = json.loads(response.choices[0].message.content)
        message_history.append({"role": "assistant", "content": json.dumps(raw_result)})

        step = raw_result.get("step")
        
        if step == "START":
            print("🔥", raw_result.get("content"))
            continue

        if step == "TOOL":
            tool_to_call = raw_result.get("tool")
            tool_input = raw_result.get("input")
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")
            
            message_history.append(
                {
                    "role": "developer", 
                    "content": json.dumps({
                        "step": "OBSERVE", 
                        "tool": tool_to_call, 
                        "input": tool_input, 
                        "output": tool_response
                })
            })
            continue

        if step == "PLAN":
            print("🧠", raw_result.get("content"))
            continue

        if step == "OUTPUT":
            print("🤖", raw_result)
            break
