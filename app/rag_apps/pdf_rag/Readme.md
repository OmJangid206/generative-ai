# PDF RAG with Qdrant

A simple Retrieval-Augmented Generation (RAG) application that ingests PDF documents, generates embeddings using HuggingFace models, stores vectors in Qdrant, and performs semantic search over PDF content.

## Project Structure

```text
.
├── Readme.md
├── data
│   └── CV - Ashok Rathore.pdf
├── ingest.py
├── main.py
└── requirements.txt
```

## Features

* Load PDF documents from a local directory
* Split PDF content into smaller chunks
* Generate embeddings using HuggingFace Sentence Transformers
* Store vectors in Qdrant
* Perform semantic similarity search
* Interactive command-line retrieval interface

## Prerequisites

* Python 3.10+
* Qdrant
* Docker (optional)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/OmJangid206/generative-ai
cd app/rag_apps/pdf_rag
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

### 4. Add PDF Documents

Place your PDF files inside the `data` directory.

Example:

```text
data/
├── CV - Ashok Rathore.pdf
├── Resume.pdf
├── Research_Paper.pdf
└── Handbook.pdf
```

## Ingest PDF Documents

Generate embeddings and create the vector index:

```bash
python3 ingest.py
```

Example output:

```text
Loading PDF documents...
Loaded 2 pages

Created 18 chunks

Document indexing completed successfully
Total vectors stored: 18
```

During ingestion the application:

1. Loads PDF files from the data directory
2. Splits content into chunks
3. Generates embeddings using HuggingFace
4. Creates a Qdrant collection
5. Stores embeddings for semantic retrieval

## Run Semantic Search

Start the retrieval application:

```bash
python3 main.py
```

Example:

```text
PDF Document Search Ready
Type 'exit' to quit.

Ask Question: What are Ashok's technical skills?

Search Results:

Result 1
Python, Django, FastAPI...

Result 2
Machine Learning, NLP...
```

Exit the application:

```text
Ask Question: exit
Exiting search...
```

## Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

## Vector Database

```text
Qdrant
```

Default collection:

```text
pdf_documents
```

Storage location:

```text
./qdrant_db
```

## Example Questions

* What are the candidate's technical skills?
* What work experience is mentioned?
* What programming languages does the candidate know?
* What projects has the candidate worked on?
* What educational qualifications are listed?
* Does the candidate have experience with machine learning?
* What soft skills are mentioned?
* Summarize the candidate's profile.

## How It Works

```text
PDF Documents
      │
      ▼
Document Loader
      │
      ▼
Text Chunking
      │
      ▼
HuggingFace Embeddings
      │
      ▼
Qdrant Vector Database
      │
      ▼
Semantic Search
      │
      ▼
Relevant PDF Chunks
```
