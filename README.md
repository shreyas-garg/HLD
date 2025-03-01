# Visit Counter Assignment

This is a starter codebase for implementing a distributed visit counter service using FastAPI, Redis, and Docker.

## Architecture Overview

The system is designed with the following components:

1. **FastAPI Application**: Handles HTTP requests and provides REST API endpoints
2. **Redis Cluster**: Multiple Redis instances for distributed storage
3. **Consistent Hashing**: For distributing keys across Redis nodes
4. **Batch Processing**: For optimizing write operations

## Setup Instructions

1. Make sure you have Docker and Docker Compose installed
2. Clone this repository
3. Run the application:
   ```bash
   docker compose up --build
   ```
4. The API will be available at `http://localhost:8000`

## Implementation Tasks

The codebase contains TODOs in various files that need to be implemented:

1. **Consistent Hashing** (`app/core/consistent_hash.py`):
   - Implement the consistent hashing ring
   - Handle node addition and removal
   - Implement key distribution

2. **Redis Manager** (`app/core/redis_manager.py`):
   - Implement connection pooling
   - Handle Redis operations with retries
   - Implement batch operations

3. **Visit Counter Service** (`app/services/visit_counter.py`):
   - Implement visit counting logic
   - Implement batch processing
   - Handle concurrent updates

## API Endpoints

- `POST /visit/{page_id}`: Record a visit
- `GET /visits/{page_id}`: Get visit count

## Testing

You can test the API using curl or any HTTP client:

```bash
# Record a visit
curl -X POST http://localhost:8000/visit/123

# Get visit count
curl http://localhost:8000/visits/123
```

## File Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── counter.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   ├── consistent_hash.py
│   │   └── redis_manager.py
│   ├── services/
│   │   └── visit_counter.py
│   ├── schemas/
│   │   └── counter.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
``` 