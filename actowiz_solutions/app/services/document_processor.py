"""
Document processing service.

Responsible for content extraction, chunk creation,
embedding generation, and vector storage.
"""
import os
import uuid
from pypdf import PdfReader

from db.qdrant_service import store_embedding
from services.embedding_service import generate_embedding
from db.sqlite_service import update_document_status

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# Extract Content
def extract_document_content(file_path: str, file_type: str) -> str:
    """
    Extract text content from a supported document.
    """
    if file_type == "pdf":
        reader = PdfReader(file_path)

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if file_type in {"txt", "py"}:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print("content[:500]", content[:500])
            return file.read()

    raise ValueError(f"Unsupported file type: {file_type}")


# def create_text_chunks(
#     text: str,
#     chunk_size: int = 500,
#     overlap: int = 100,
# ) -> list[str]:
#     """
#     Split text into overlapping chunks.
#     """
#     chunks = []
#     start = 0

#     while start < len(text):
#         chunks.append(text[start : start + chunk_size])
#         start += chunk_size - overlap

#     return chunks


def create_text_chunks(
    text: str,
    file_type: str,
) -> list[str]:

    if file_type in ("py", "txt"):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\nclass ",
                "\ndef ",
                "\n\n",
                "\n",
                " "
            ]
        )

    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\nclass ",
                "\n    def ",
                "\ndef ",
                "\n\n",
                "\n",
            ]
        )

    return splitter.split_text(text)
 
 
 
def process_document(
    document_id: str,
    file_path: str,
    file_type: str,
) -> None:
    """
    Process a document and store chunk embeddings.
    """

    try:
        
        # Extract document content
        content = extract_document_content(file_path, file_type)
        
        # Create text chunks
        chunks = create_text_chunks(content)

        # Store embeddings into the Qdrant DB
        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            store_embedding(
                point_id=str(uuid.uuid4()),
                embedding=embedding,
                payload={
                    "document_id": document_id,
                    "filename": file_path.split("/")[-1],
                    "file_type": file_type,
                    "chunk_index": index,
                    "content": chunk,
                },
            )

        # Update document status in Sqlite3
        update_document_status(document_id, "completed")
        
        # Delete temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        print(f"Failed to process documents: {str(e)}")
        update_document_status(document_id, "failed")
        raise
