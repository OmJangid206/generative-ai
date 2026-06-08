# Load ChromaDB
# Search documents
# Ask questions

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient

PDF_DIR = "data"
COLLECTION_NAME = "pdf_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

client = QdrantClient(path="./qdrant_db")

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

while True:

    query = input("\nAsk Question: ")

    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)

    print("\nResults:\n")

    for i, doc in enumerate(docs, start=1):
        print(f"Result {i}")
        print(doc.page_content[:1000])
        print()
