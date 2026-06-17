"""
PDF Indexing Pipeline with Qdrant Vector Database

This script performs the complete document ingestion workflow:

1. Load PDF documents from a local directory
2. Split documents into smaller text chunks
3. Generate vector embeddings using a HuggingFace model
4. Create a Qdrant vector collection
5. Store document embeddings in Qdrant
6. Perform semantic similarity search for testing

Requirements:
- LangChain
- HuggingFace Embeddings
- Qdrant
- PyPDF

Output:
- Persistent local Qdrant database
- Searchable vector index of PDF content
"""

from uuid import uuid4

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


# Configuration
PDF_DIR = "data"
COLLECTION_NAME = "pdf_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QDRANT_DB_PATH = "./qdrant_db"

# Load PDF Documents
print("Loading PDF documents...")

loader = PyPDFDirectoryLoader(PDF_DIR)
documents = loader.load()

print(f"Loaded {len(documents)} pages")

# Split Documents into Chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# Initialize Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

# Connect to Qdrant
# Reference: https://docs.langchain.com/oss/python/integrations/vectorstores/qdrant
# client = QdrantClient(":memory:")
client = QdrantClient(path=QDRANT_DB_PATH)

# Create Fresh Collection
# Remove existing collection to avoid duplicate
# indexing during development.

if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384, 
        distance=Distance.COSINE
    ),
)

# Initialize Vector Store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

# Index Document Chunks
uuids = [str(uuid4()) for _ in range(len(chunks))]

vector_store.add_documents(
    documents=chunks, 
    ids=uuids
)

print("Document indexing completed successfully")

# Verify Indexed Records
print(
    f"Total vectors stored: "
    f"{client.count(COLLECTION_NAME).count}"
)


if __name__== "__main__":
    # Test Semantic Search
    query = 'Soft Skills:'

    results = vector_store.similarity_search(
        query=query, 
        k=3
    )

    for index, result in enumerate(results, start=1):
        # print(f"\nResult {index}")
        print(result.page_content)