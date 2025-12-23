import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# client = OpenAI()

# response = client.responses.create(
#     model="gpt-5",
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# print(response.output_text)

# -------------------------------------
client = OpenAI(
    api_key=OPENAI_API_KEY
)
response = client.responses.create(
    model="gpt-4o-mini",
    input="Write the short bedtime story about a unicorn",
)

# print(response)
print(response.output_text)