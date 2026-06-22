# System Design

## Overview

The platform enables internal developers to:

1. Upload documents and code files
2. Perform semantic search
3. Delete documents
4. Access LLMs through a centralized AI Gateway

## Components

### FastAPI

Handles API requests.

### Redis

Message broker for Celery.

### Celery Worker

Processes documents asynchronously.

### Qdrant

Stores embeddings and chunk metadata.

### SQLite

Stores document metadata and query logs.

## Processing Flow

Upload
→ FastAPI
→ SQLite Metadata
→ Redis Queue
→ Celery Worker
→ Chunking
→ Embedding Generation
→ Qdrant

## Query Flow

User Query
→ Query Embedding
→ Qdrant Search
→ Ranked Chunks

## AI Gateway Flow

User Query
→ Semantic Search
→ Context Construction
→ LLM Provider
→ Response