# Chroma db references
# http://docs.trychroma.com/docs/overview/getting-started
# https://docs.trychroma.com/docs/run-chroma/clients#in-memory-client
# http://docs.trychroma.com/docs/run-chroma/client-server

import os
from dotenv import load_dotenv # type: ignore
from openai import OpenAI # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
import chromadb  # type: ignore
from pypdf import PdfReader # type: ignore

# Load ENV
load_dotenv()

# Open Router client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

MODEL= "google/gemini-2.0-flash-001"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Embedding Model
embed_model = SentenceTransformer(EMBED_MODEL)

# Chroma DB (in-memory)
# chroma_client = chromadb.Client()

# Chroma DB (local persistent storage)
# chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Chroma DB (Client Server)
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# Create Collection
# collection = chroma_client.create_collection(
#     name="multi_pdf_collection"
# )
collection = chroma_client.get_or_create_collection(
    name="multi_pdf_collection"
)

print("Before:", collection.count())

# Read PDFs
PDF_FOLDER = "pdfs"

documents = []
ids = []
metadatas = []
chunk_id = 0

for file in os.listdir(PDF_FOLDER):
    
    if not file.endswith("pdf"):
        continue
    
    pdf_path = os.path.join(PDF_FOLDER, file)
    print(f"Loading {file}")
    
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for page in reader.pages:
        
        text = page.extract_text()
        if text:
            full_text += text + "\n"
        
    # Chunking
    chunk_size = 500
    for i in range(0, len(full_text), chunk_size):
        chunk = full_text[i:i+chunk_size]
        documents.append(chunk)
        ids.append(str(chunk_id))
        
        metadatas.append({"source": file})
        chunk_id += 1

embeddings = embed_model.encode(
    documents
).tolist()

# Store chunks in db
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)

# print(f"Total Chunks: {len(documents)}")
# print("After:", collection.count())
# data = collection.get()
# print(data["ids"])
data = collection.get(include=["embeddings", "documents", "metadatas"])
print(data)
# print(data.keys())
# print(chroma_client.list_collections())


# ---------------------------------------------------
# ---------------------------------------------------
# Chat Bot
print("Multi PDF chatbot Started")
print("Type exit to stop\n")

while True:
    
    user_query = input("Ask anything: ")
    
    if user_query.lower() == "exit":
        print("Chat-bot exit.")
        break

    query_embedding = embed_model.encode(
        user_query
    ).tolist()

    # Retrieve top chunks
    results = collection.query(
        # query_texts=[user_query],
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    retrieved_docs = results["documents"][0]
    retrieved_meta = results["metadatas"][0]
    
    context = ""
    sources = set()
    
    for doc, meta in zip(retrieved_docs, retrieved_meta):
        
        context += doc + "\n"
        sources.add(meta["source"])
        
    
    prompt = f"""
        You are a PDF assistant.
        Answer ONLY using the provided context.
        If the answer is not present in the context, reply:
        "Could not find the information."
        CONTEXT: {context}
    """
    messages = [
        {
        "role":"system",
        "content": prompt
        },
        {
            "role": "user",
            "content": user_query  
        }
    ]
        
    try:
        
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        
        print("\nBot: ",end="")
        
        full_reply = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                full_reply += text

        print("\n")
        for src in sources:
            print(f"source: {src}")
        print()

    except Exception as err:
        print(f"Error: {str(err)}")


# # Run Chroma DB Client server
# # chroma run --host 0.0.0.0 --port 8000
