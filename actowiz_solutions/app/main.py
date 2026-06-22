"""
main.py

This module initializes the FastAPI application, registers all API routers,
and exposes the health-check endpoint used for service monitoring.

Routes:
    - /documents : Document management APIs
    - Query APIs
    - Gateway APIs
"""

import uvicorn
from fastapi import FastAPI

from routes.document_routes import router as document_router
from routes.gateway_routes import router as gateway_router
from db.sqlite_service import initialize_database
from db.qdrant_service import create_collection

# Create tables/ collection if not exits
initialize_database()
create_collection()

# initializes App
app = FastAPI()


# Register API routes
app.include_router(document_router)
# app.include_router(gateway_router, prefix="/gateway")


@app.get("/")
def ping():
    """
    Health check endpoint.
    """
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
