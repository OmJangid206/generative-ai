import os
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader

# ==============================
# Load ENV
# ==============================
load_dotenv()

# ==============================
# OpenRouter Client
# ==============================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

# ==============================
# Select Model
# ==============================
MODEL = "google/gemini-2.0-flash-001"

# Examples:
# MODEL = "openai/gpt-4o-mini"
# MODEL = "anthropic/claude-3.5-sonnet"
# MODEL = "meta-llama/llama-3.3-70b-instruct"

# ==============================
# Load PDF Text
# ==============================
def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text

# ==============================
# Choose PDF
# ==============================
pdf_path = input("Enter PDF path: ")

if not os.path.exists(pdf_path):

    print("PDF file not found.")
    exit()

print("\nReading PDF...\n")

pdf_text = read_pdf(pdf_path)

print("PDF Loaded Successfully.\n")

# ==============================
# System Prompt
# ==============================
SYSTEM_PROMPT = f"""
You are a helpful PDF assistant.

Answer ONLY from the PDF content below.

If answer is not available in PDF, say:
"I could not find that in the PDF."

PDF CONTENT:
{pdf_text}
"""

# ==============================
# Messages Memory
# ==============================
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

print("📘 PDF Chatbot Started")
print("Type 'exit' to stop\n")

# ==============================
# Chat Loop
# ==============================
while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("\nChat ended.")
        break

    messages.append({
        "role": "user",
        "content": question
    })

    try:

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

        messages.append({
            "role": "assistant",
            "content": full_reply
        })

    except Exception as e:

        print(f"\nError: {e}\n")