"""
document_routes.py

Document API routes.
"""

from fastapi import APIRouter, UploadFile, File
from controllers.document_controller import(
    upload_document, delete_document, query_document
)


router = APIRouter()


@router.post("/documents")
async def upload_document_route(file: UploadFile = File(...)):
    """
    Upload a document for processing.
    """
    return await upload_document(file)


@router.delete("/documents/{document_id}")
async def remove_document(document_id: str):
    """
    Delete document embeddings and metadata.
    """
    return await delete_document(document_id)


@router.post("/query")
async def query_documents(payload: dict):
    """
    Perform semantic search across uploaded documents
    and return the most relevant chunks.
    """
    return await query_document(payload)

# ------------------------------------------
# POST /documents
# Request: file = sample.pdf
# Response:
# {
#     "document_id": "4f56e3a5-9d58-4cb8-a4b4-6f68f94a8c12",
#     "status": "UPLOADED",
#     "message": "Document accepted for processing"
# }

# Questions
# Why async processing?
# PDF parsing and embedding generation are expensive.
# API returns immediately while Celery processes in background.
# Why return document_id?
# Used later for delete and status tracking.

# ------------------------------------------
# POST /query
# Request:
# {
#     "query": "How do I reset my password?",
#     "limit": 5
# }

# Request with Metadata Filter
# {
#     "query": "How do I reset my password?",
#     "limit": 5,
#     "metadata_filters": {
#         "file_type": "pdf"
#     }
# }

# Response:
# {
#     "query": "How do I reset my password?",
#     "results": [
#         {
#             "score": 0.94,
#             "document_id": "123",
#             "content": "To reset password...",
#             "chunk_index": 2
#         },
#         {
#             "score": 0.89,
#             "document_id": "456",
#             "content": "Password reset process...",
#             "chunk_index": 5
#         }
#     ]
# }

# Possible Questions
# How does semantic search work?
# Query → Embedding → Qdrant similarity search → Top K chunks.
# Why score?
# Similarity score used for ranking.
# Why metadata filter?
# Search only PDFs, specific document types, etc.

# ------------------------------------------
# DELETE /documents/{document_id}
# Example: DELETE /documents/4f56e3a5-9d58-4cb8-a4b4-6f68f94a8c12

# Response
# {
#     "status": "success",
#     "document_id": "4f56e3a5-9d58-4cb8-a4b4-6f68f94a8c12"
# }
# ------------------------------------------