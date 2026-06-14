"""
Document Retrieval System

This module connects to a Qdrant vector database and enables
semantic search over indexed documents using LangChain's
retriever interface.

Workflow:
    1. Initialize embedding model
    2. Connect to Qdrant collection
    3. Create retriever
    4. Accept user queries
    5. Retrieve and display relevant documents
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "multi_documents"
TOP_K_RESULTS = 4

# Embedding Model
def initialize_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},
    )
    

# Vector Store
def initialize_vector_store(embeddings):
    """
    Connect to the Qdrant vector database and initialize
    the vector store.
    """
    client = QdrantClient(url=QDRANT_URL)
    
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
    
# Retriever - https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/as_retriever
def initialize_retriever(vector_store):
    """
    Create a retriever instance from the vector store.
    """
    return vector_store.as_retriever(
        search_kwargs={"k": TOP_K_RESULTS}
    )


def search_documents(query: str, retriever):
    """
    Retrieve relevant documents for a user query.
    """
    return retriever.invoke(query)

def display_results(documents):
    """
    Display retrieved documents.
    """
    if not documents:
        print("No relevant documents found.")
        return
    
    print("Retrieved Documents")
    print("-------------------------------------------")
    for index, document in enumerate(documents, start=1):
        print(f"\nResult #{index}")
        print("------------------------------------------")
        source = document.metadata.get("source", "Unknown")
        print(f"Source: {source}")
        print(f"Content:\n{document.page_content[:1000]}")
        print()

        
# Main Application
def main():
    """
    Run the interactive document retrieval application.
    """

    print("Document Retrieval System")
    print("Initializing embedding model...")
    embeddings = initialize_embeddings()
    
    print("Connecting to Qdrant...")
    vector_store = initialize_vector_store(embeddings)
    
    print("Creating retriever...")
    retriever = initialize_retriever(vector_store)
    
    print("Type 'exit' to quit.\n")
    
    while True:
        
        query = input("Ask Question: ").strip()
        
        if not query:
            continue
        
        if query.lower() == "exit":
            print("Shutting down retrieval system...")
            break
        
        documents = search_documents(
            query=query, 
            retriever=retriever
        )
        
        display_results(documents)
        
if __name__ == "__main__":
    main()