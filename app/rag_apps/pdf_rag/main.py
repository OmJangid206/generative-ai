"""
Load documents from an existing Qdrant vector database
and perform semantic search using LangChain.

Features:
- Connects to a local Qdrant database
- Uses HuggingFace embeddings
- Retrieves the top 3 most relevant document chunks
- Interactive question-answer search loop
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Configuration
COLLECTION_NAME = "pdf_documents"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QDRANT_DB_PATH = "./qdrant_db"

# Initialize Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME
)

# Connect to Qdrant Database
client = QdrantClient(
    path=QDRANT_DB_PATH
)

# Load Existing Vector Store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

# Create Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# Interactive Search Loop

print("PDF Document Search Ready")
print("Type 'exit' to quit.\n")

while True:

    query = input("Ask Question: ").strip()

    if query.lower() == "exit":
        print("Exiting search...")
        break

    # Perform semantic similarity search
    docs = retriever.invoke(query)

    print("\nSearch Results:\n")
    print("-----------------------------")
    for index, doc in enumerate(docs, start=1):
        print(f"\nResult {index}")
    
        # Display first 1000 characters of the retrieved chunk
        print(doc.page_content[:1000])

    print("-----------------------------")
