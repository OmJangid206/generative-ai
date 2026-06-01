
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# load API Key
load_dotenv()

# Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

MODEL = "openai/gpt-4o-mini"

# website scaper function
def scrape_website(url):
    
    try:
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url=url, headers=headers, timeout=60)

        bsoup_response = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary tags
        for tag in bsoup_response(["script", "style", "noscript"]):
            tag.decompose()

        text = bsoup_response.get_text(separator="\n")

        # Clean text
        lines = [line.strip() for line in text.splitlines()]        
        lines = [line for line in lines if line]
        text = "\n".join(lines)
        print(f"text: {text}")

        return text[:20000] 
        
    except Exception as err:
        return f"Error scraping website: {err}"


# ----------------------------------
# Website URL
URL = input("Enter Website URL: ")

print("\nScaping website...")
website_content = scrape_website(URL)

print("Website loaded successfully!\n")

# System Prompt
SYSTEM_PROMPT = f"""
You are a website Assistant.
Answer questions ONLY using the website content below.
If answer is not found in website content.
say: 'I could not find that information on the website.'

WEBSITE CONTENT: {website_content}
"""

messages = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]

print("Website Chatbot Ready (type exit to stop)\n")

while True:
    query = input("Ask Question: ")
    
    if query.lower() == "exit":
        print("Chat bot has been stoped.")
        break
    
    messages.append({
        "role": "user",
        "content": query
    })

    response = client.chat.completions.create(
        model=MODEL, messages=messages
    )
    
    answer = response.choices[0].message.content
    
    print("\nBot: ", answer)
    print()
    
    messages.append({
        "role": "assistant",
        "content": answer
    })
