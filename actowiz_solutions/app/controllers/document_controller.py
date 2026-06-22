"""
document_worker.py

Document upload controller.
Handles document validation, file storage, and background
processing task submission.
"""

import os
import uuid
import time

from fastapi import UploadFile, File, HTTPException
from workers.document_worker import process_document_task
from services.embedding_service import generate_embedding
from db.qdrant_service import search_document, delete_document_embeddings
from db.sqlite_service import insert_document, delete_document_metadata, log_query


# Upload Documents
async def upload_document(file: UploadFile = File(...)):

    ALLOWED_EXTENSIONS = {"pdf", "txt", "docx", "py"}
    UPLOAD_DIR = "public/temp"

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Load file in the local system
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    document_id = str(uuid.uuid4())
    filename = f"{document_id}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Store metadata in the Sqlite3
    insert_document(
        document_id=document_id,
        filename=file.filename,
        file_type=extension,
    )

    # Load file in background using celery worker
    process_document_task.delay(document_id, file_path, extension)

    return {
        "document_id": document_id,
        "status": "UPLOADED",
        "message": "Document accepted for processing",
    }


# Query Docuemnts
async def query_document(payload):

    try:
        query = payload.get("query")
        limit = payload.get("limit", 5)
        metadata_filters = payload.get(
            "metadata_filters"
        )
        
        if not query:
            raise HTTPException(
                status_code=400,
                detail="Query is required"
            )

        start_time = time.time()
        
        vector = generate_embedding(query)

        results = search_document(
            query_vector=vector,
            limit=limit,
            metadata_filters=metadata_filters
        )
    
        execution_time = (time.time() - start_time)
        log_query(query, execution_time,)

        response = []

        for item in results:

            response.append({
                "score": item.score,
                "document_id": item.payload.get("document_id"),
                "content": item.payload.get("content"),
                "chunk_index": item.payload.get("chunk_index"),        
            })

        return {
            "query": query,
            "results": response
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Delete Documents
async def delete_document(document_id: str):

    if not document_id or not document_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid document_id"
        )

    try:
        deleted_rows = delete_document_metadata(document_id)

        if deleted_rows == 0:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        delete_document_embeddings(document_id)

        return {
            "status": "success",
            "document_id": document_id
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )