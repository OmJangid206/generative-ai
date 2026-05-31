import os
from dotenv import load_dotenv
from openai import OpenAI
# from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader

# Load ENV
load_dotenv()

# Open Router client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)

MODEL= "google/gemini-2.0-flash-001"
EMBED_MODEL = "all-MiniLM-L6-v2"

# # Embedding Model
# embed_model = SentenceTransformer(EMBED_MODEL)



# Chroma DB
# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Collection
# collection = chroma_client.create_collection(
#     name="multi_pdf_collection"
# )
collection = chroma_client.get_or_create_collection(
    name="multi_pdf_collection"
)

# Read PDFs
# PDF_FOLDER = "pdfs"

# documents = []
# ids = []
# metadatas = []
# chunk_id = 0

# for file in os.listdir(PDF_FOLDER):
    
#     if not file.endswith("pdf"):
#         continue
    
#     pdf_path = os.path.join(PDF_FOLDER, file)
#     print(f"Loading {file}")
    
#     reader = PdfReader(pdf_path)
#     full_text = ""
    
#     for page in reader.pages:
        
#         text = page.extract_text()
#         if text:
#             full_text += text + "\n"
        
#     # Chunking
#     chunk_size = 500
#     for i in range(0, len(full_text), chunk_size):
#         chunk = full_text[i:i+chunk_size]
#         documents.append(chunk)
#         ids.append(str(chunk_id))
        
#         metadatas.append({"source": file})
#         chunk_id += 1

# # Store chunks in db
# collection.add(
#     documents=documents,
#     ids=ids,
#     metadatas=metadatas
# )

# # print(f"Total Chunks: {len(documents)}")
# print(collection.count())
# # print(collection.get())
# data = collection.get(include=["embeddings", "documents", "metadatas"])
# # print(data)
# print(data.keys())

# Chat Bot
print("Multi PDF chatbot Started")
print("Type exit to stop\n")

while True:
    
    user_query = input("Ask anything: ")
    
    if user_query.lower() == "exit":
        print("Chat-bot exit.")
        break

    # Retrieve top chunks
    results = collection.query(
        query_texts=[user_query],
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
