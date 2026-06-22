# Database Design

## Documents

SQLite

Fields:

- id
- filename
- file_type
- status
- created_at
- is_deleted

## Query Logs

SQLite

Fields:

- id
- query
- execution_time
- created_at

## Chunks

Stored as Qdrant payload.

Payload:

{
  "document_id": "...",
  "file_type": "pdf",
  "chunk_index": 0,
  "content": "..."
}

## Embeddings

Stored in Qdrant vectors.

Vector Size:
384

Model:
all-MiniLM-L6-v2

## Indexing Strategy

SQLite:
- Primary Key on id

Qdrant:
- HNSW vector index
- Payload filtering

## Metadata Modeling

- document_id
- filename
- file_type
- chunk_index
- content

## Query Patterns

Upload
Search
Delete

## Caching

Current:
- Model cached in memory

Future:
- Redis query cache