# API Design

## Upload Document

POST /documents

Request:
multipart/form-data

file=<document>

Response:

{
  "document_id": "...",
  "status": "UPLOADED"
}

---

## Query Documents

POST /query

Request:

{
  "query": "How do I reset my password?",
  "limit": 5
}

Response:

{
  "query": "...",
  "results": [
    {
      "score": 0.92,
      "document_id": "...",
      "content": "...",
      "chunk_index": 0
    }
  ]
}

---

## Delete Document

DELETE /documents/{id}

Response:

{
  "status": "success",
  "document_id": "..."
}

---

## AI Gateway

POST /gateway/chat

Request:

{
  "provider": "openai",
  "query": "Explain document"
}

Response:

{
  "provider": "openai",
  "response": "..."
}