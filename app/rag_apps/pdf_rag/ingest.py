# Load PDF
# Chunk text
# Create embeddings
# Store in Qdrant DB

import uuid
from uuid import uuid4
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams


PDF_DIR = "data"
COLLECTION_NAME = "pdf_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading PDFs...")

# Load PDFs
loader = PyPDFDirectoryLoader(PDF_DIR)
documents = loader.load()
print(f"Loaded {len(documents)} pages")

# Splits text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20
)

chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

# Initialize model
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME
)

# reference: https://docs.langchain.com/oss/python/integrations/vectorstores/qdrant
# QdrantVectorStore.from_documents(
#     documents=chunks,
#     embedding=embeddings,
#     path="./qdrant_db",

# client = QdrantClient(":memory:")
client = QdrantClient(path="./qdrant_db")

if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

uuids = [str(uuid4()) for _ in range(len(chunks))]

vector_store.add_documents(documents=chunks, ids=uuids)

print("Documents indexed success")
print(client.count(COLLECTION_NAME))

query = 'Soft Skills:'

result = vector_store.similarity_search(query=query, k=3)

for res in result:
    print(f"{res.page_content}")