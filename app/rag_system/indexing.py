from pathlib import Path
import os
from dotenv import load_dotenv
 
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

pdf_path = Path(__file__).parent / "nodejs.pdf"

# Load this file in the python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)

# Vecoter Embeddings
# embedding_model = GoogleGenerativeAIEmbeddings(
#     model="models/gemini-embedding-001",
#     api_key=os.environ['GEMINI_API_KEY']

# )

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    force_recreate=True
)

vector_db = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="learning_rag",
    url="http://localhost:6333",
)

print("Indexing of documents done....")

# pip install langchain-qdrant
# pip install sentence-transformers

# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_qdrant import QdrantVectorStore
# from langchain_community.embeddings import HuggingFaceEmbeddings

# pdf_path = Path(__file__).parent / "nodejs.pdf"

# loader = PyPDFLoader(pdf_path)
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1500,
#     chunk_overlap=100
# )
# chunks = text_splitter.split_documents(docs)

# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# vector_db = QdrantVectorStore.from_documents(
#     documents=chunks,
#     embedding=embedding_model,
#     collection_name="learning_rag",
#     url="http://localhost:6333",
# )

# print("Indexing of documents done 🚀")

