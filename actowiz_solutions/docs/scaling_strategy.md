# Scaling Strategy

## Current Scale

~100 Internal Developers

## Horizontal Scaling

FastAPI
- Multiple instances behind load balancer

Celery
- Multiple workers

Redis
- Shared broker

Qdrant
- Cluster mode

## Reliability

- Async processing
- Retry failed jobs
- Document status tracking

## Failure Handling

Upload Failure
→ status = failed

Processing Failure
→ Celery retry

Delete Failure
→ Return error response

## Tradeoffs

SQLite
Pros:
- Simple
- Lightweight

Cons:
- Not ideal for large scale

Future:
PostgreSQL

## Future Enhancements

- Authentication
- Authorization
- Monitoring
- Distributed Qdrant
- LLM Provider Routing