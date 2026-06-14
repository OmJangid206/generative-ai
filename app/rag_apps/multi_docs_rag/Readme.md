# Multi-Document RAG with Qdrant

A simple Retrieval-Augmented Generation (RAG) application that ingests multiple document formats, generates embeddings using HuggingFace models, stores vectors in Qdrant, and performs semantic search.

## Project Structure

```text
.
├── Readme.md
├── data
│   └── docs
│       ├── contract.jpg
│       ├── employees.csv
│       ├── invoice.png
│       ├── notes.txt
│       ├── policy.docx
│       ├── report.pdf
│       └── sales.xlsx
├── ingest.py
├── main.py
└── requirements.txt
```

## Supported File Types

* PDF (`.pdf`)
* Word Documents (`.docx`)
* Text Files (`.txt`)
* CSV Files (`.csv`)
* Excel Files (`.xlsx`, `.xls`)
* Images with OCR (`.png`, `.jpg`, `.jpeg`)

## Prerequisites

* Python 3.10+
* Docker
* Qdrant

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/OmJangid206/generative-ai
cd app/rag_apps/multi_docs_rag
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Qdrant

This project uses **Qdrant** as the vector database for storing document embeddings and performing semantic search.

For Qdrant installation and setup, refer to the official Qdrant Quickstart Guide:

[Qdrant Quickstart Documentation](https://qdrant.tech/documentation/quick-start/?utm_source=chatgpt.com)

#### Pull the Qdrant Docker Image

```bash
docker pull qdrant/qdrant
```

#### Run Qdrant Container

```bash
docker run -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

This command:

* Starts Qdrant on port `6333`
* Persists vector data inside the `qdrant_storage` directory
* Makes the database available at `http://localhost:6333`

Qdrant Docker setup and storage recommendations are documented in the official Qdrant Quickstart guide.

#### Verify Qdrant is Running

```bash
curl http://localhost:6333
```

Expected response:

```json
{
  "title": "qdrant - vector search engine",
  "version": "x.x.x"
}
```

#### Qdrant Dashboard

Open the Qdrant dashboard in your browser:

```text
http://localhost:6333/dashboard
```

The dashboard allows you to inspect collections, vectors, and stored payloads directly from the browser.


### 5. Add Documents

Place your documents inside:

```text
data/docs/
```

Example:

```text
data/docs/
├── report.pdf
├── policy.docx
├── notes.txt
├── employees.csv
├── sales.xlsx
├── invoice.png
└── contract.jpg
```

## Ingest Documents

Generate embeddings and store vectors in Qdrant:

```bash
python3 ingest.py
```

Example output:

```text
STEP 1: Loading documents...
Loaded 8 document records.

STEP 2: Creating chunking...
Generated 22 document chunks

STEP 3: Initializing embeddings...

STEP 4: Storing vectors in Qdrant...
Stored 22 chunks into Qdrant collection multi_documents

Document ingestion completed.
```

## Run Semantic Search

Start the retrieval application:

```bash
python3 main.py
```

Example:

```text
Ask Question: What is the company policy?

Retrieved Documents
------------------------------------------------------------

Result #1
Source: policy.docx
...
```

Exit the application:

```text
Ask Question: exit
```

## Embedding Model

```text
sentence-transformers/all-mpnet-base-v2
```

## Vector Database

```text
Qdrant
```

Default collection:

```text
multi_documents
```


# Example Questions
* Question for testing RAG
* What is the maternity leave policy?
* Who works in the Finance department?
* What was the revenue in April?
* What is the budget for Project Phoenix?
* What is the amount on Invoice #1001?
* What salary is mentioned in the employment contract?
