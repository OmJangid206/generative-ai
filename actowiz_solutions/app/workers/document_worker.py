"""
Celery worker responsible for background document processing.
"""

from celery import Celery
from services.document_processor import process_document


celery = Celery(
    "document_worker", 
    broker="redis://localhost:6379/0"
)


@celery.task
def process_document_task(
    document_id: str,
    file_path: str,
    file_type: str,
) -> None:
    """
    Execute document processing in the background.
    """
    process_document(
        document_id=document_id, 
        file_path=file_path, 
        file_type=file_type
    )
