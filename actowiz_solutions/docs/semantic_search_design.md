# Semantic Search Design

## Chunking Strategy

PDF/Text Documents:

* Recursive chunking
* Chunk Size: 500
* Overlap: 100

Code Files:

* Function/Class aware chunking
* Chunk Size: 1000
* Overlap: 200

## Embedding Lifecycle

Document
→ Chunk
→ Generate Embedding
→ Store in Qdrant

Query
→ Generate Query Embedding
→ Similarity Search
→ Retrieve Top-K Chunks

## Similarity Search

Vector Database:
Qdrant

Distance Metric:
Cosine Similarity

## Ranking Strategy

Results ranked using:

* Vector similarity score
* Metadata filters

## Failure Handling

Upload Failure:

* Status updated to failed

Worker Failure:

* Retry via Celery

Delete Failure:

* Return error response

## Soft Delete vs Hard Delete

Soft Delete:

* Set is_deleted = 1
* Data remains recoverable

Hard Delete:

* Delete SQLite metadata
* Delete Qdrant embeddings
* Delete temporary files

Current Implementation:
Hard Delete
