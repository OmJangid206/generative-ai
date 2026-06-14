from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai
import os
# Vector Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    api_key=os.environ['GEMINI_API_KEY']
)


vector_db = QdrantVectorStore.from_existing_collection(
    embeddings=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

# Take user input
user_query = input("Ask somthing: ")

# Relevant chunks from thr vector db
search_results = vector_db.similarity_search(user_query)

print(f"ddddd: {search_results}")
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""
 You are an export AI Assistant who answers user query based on the avaialble context retrieved from a PDF file along with page_contents and page number.
 
 You should only answers the user based on the following context and nagivate the user to open the right page number to know more.
 
 Context: 
 {context}
"""

# Model configuration
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"

client  = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[
        {
            "role": "user",
            "parts": [
                {"text": SYSTEM_PROMPT},
                {"text": user_query}
            ]
        }
    ]
    
)

print(f"response: {response}")


