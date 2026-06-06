# pip install fastapi uvicorn openai python-multipart pdfplumber

import os
import json
import pdfplumber
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from openai import OpenAI

# Load Env
load_dotenv()

# Initialize app
app = FastAPI()

# Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPEN_ROUTER_API"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def analyse_resume(resume_text):

    prompt = f"""
    Analyze the following resume.
    
    Return response in JSON format:
    
    {{
        "ats_score": number
        "strengths": [],
        "weaknesses": [],
        "missing_keywords": [],
        "recommendations": []
    }}
    
    Resume: {resume_text}
    """

    # Messages
    messages = [
        {"role": "system", "content": "You are an expert ATS and resume reviewer."},
        {"role": "user", "content": prompt},
    ]

    # Response
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )
    print(f"response: {response}")

    result = json.loads(
        response.choices[0].message.content
    )
    return result


def extract_pdf_text(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


@app.post("/analyze-resume")
async def analyze_resume_api(file: UploadFile = File(...)):

    try:
        # file path
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        resume_text = extract_pdf_text(file_path)

        result = analyse_resume(resume_text)
        return {"status": "success", "analysis": result}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "failed", "analysis": f"Error: {str(e)}"}


# Run Application
# Run - uvicorn resume_analyzer:app --reload
# Open - http://127.0.0.1:8000/docs