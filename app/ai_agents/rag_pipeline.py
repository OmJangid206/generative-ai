# Simple RAG (Retrieval-Augmented Generation) Pipeline in Python
# Install first:
# pip install openai faiss-cpu sentence-transformers python-dotenv numpy

import os
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenRouter / OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API")
)

# Embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample knowledge base (documents)
documents = [
    "Python is a popular programming language used for web development and AI.",
    "RAG stands for Retrieval-Augmented Generation.",
    "FAISS is a library used for efficient similarity search.",
    "OpenRouter helps access multiple AI models using one API."
]

print("Creating embeddings...")

# Convert documents to embeddings
embeddings = embedding_model.encode(documents)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("Simple RAG Chatbot Started! Type 'exit' to quit.\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        print("Bot: Goodbye!")
        break

    # Convert user query to embedding
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search top matching document
    distances, indices = index.search(query_embedding, k=2)

    retrieved_docs = [documents[i] for i in indices[0]]
    context = "\n".join(retrieved_docs)

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        print("\nRetrieved Context:")
        for doc in retrieved_docs:
            print("-", doc)

        print("\nBot:", answer)
        print()

    except Exception as e:
        print("Error:", str(e))