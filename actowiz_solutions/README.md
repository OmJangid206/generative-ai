# Internal AI Knowledge Platform

Backend platform for document ingestion, semantic search, and AI-powered knowledge retrieval.

## Features

- Upload Documents (PDF, TXT, Code Files)
- Asynchronous Document Processing
- Semantic Search using Qdrant
- Metadata Filtering
- Document Deletion
- AI Gateway Integration
- Query Logging

## Tech Stack

- FastAPI
- Celery
- Redis
- Qdrant
- SQLite
- SentenceTransformers

##


# Setup & Installation

## Prerequisites

* Python 3.11+
* Docker
* Redis
* Qdrant

## Clone Repository

```bash
git clone <repository-url>
cd actowiz_solutions
```

## Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate Virtual Environment:

### Mac/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Qdrant

```bash
docker run -d \
--name qdrant \
-p 6333:6333 \
qdrant/qdrant
```

Verify:

```bash
http://localhost:6333/dashboard
```

## Start Redis

```bash
docker run -d \
--name redis \
-p 6379:6379 \
redis
```

Verify:

```bash
docker exec -it redis redis-cli ping
```

Expected Output:

```bash
PONG
```

## Start Celery Worker

```bash
cd app
celery -A workers.document_worker worker --pool=solo --loglevel=info
```

Expected Output:

```text
[tasks]
  . workers.document_worker.process_document_task
```

## Start FastAPI Application

Open a new terminal:

```bash
cd app
uvicorn main:app --reload
```

OR

```bash
cd app
python -m uvicorn main:app
```

Application URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```


# Documentation

Detailed design documents are available in the docs directory:

* api_design.md
* database_design.md
* semantic_search_design.md
* scaling_strategy.md
* system_design.md


## Future Improvements

- PostgreSQL
- Redis Query Cache