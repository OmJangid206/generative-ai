import sqlite3
from datetime import datetime

DB_NAME = "documents.db"


CREATE__DOCUMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    filename TEXT,
    file_type TEXT,
    status TEXT,
    created_at TEXT,
    is_deleted INTEGER DEFAULT 0
)
"""

CREATE_QUERY_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    execution_time REAL,
    created_at TEXT
)
"""
        
INSERT_DOCUMENT_QUERY = """
INSERT INTO documents
(id, filename, file_type, status, created_at)
VALUES (?, ?, ?, ?, ?)
"""

DELETE_DOCUMENT_QUERY = """
DELETE FROM documents
WHERE id = ?
"""

UPDATE_DOCUMENT_STATUS_QUERY = """
UPDATE documents
SET status = ?
WHERE id = ?
"""

INSERT_QUERY_LOG_QUERY = """
INSERT INTO query_logs
(query, execution_time, created_at )
VALUES (?, ?, ?)
"""

UPDATE_DOCUMENT_STATUS_QUERY = """
UPDATE documents
SET status = ?
WHERE id = ?
"""


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Documents table
    cursor.execute(CREATE__DOCUMENTS_TABLE)

    # Create Query logs table
    cursor.execute(CREATE_QUERY_LOGS_TABLE)

    conn.commit()
    conn.close()

# Insert document
def insert_document(document_id, filename, file_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        INSERT_DOCUMENT_QUERY,
        (
            document_id, filename, file_type, 
            "processing",
            datetime.now().isoformat()
        ),
    )

    conn.commit()
    conn.close()

# Delete document metadata
def delete_document_metadata(document_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        DELETE_DOCUMENT_QUERY,
        (document_id,),
    )

    deleted_rows = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_rows

# Log Query
def log_query(query, execution_time,):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        INSERT_QUERY_LOG_QUERY,
        (
            query,
            execution_time,
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


# Update document status
def update_document_status(
    document_id: str,
    status: str,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        UPDATE_DOCUMENT_STATUS_QUERY,
        (status, document_id),
    )

    conn.commit()
    conn.close()
