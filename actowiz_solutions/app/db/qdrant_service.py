"""
Qdrant database service.

Provides helper functions for storing and retrieving
vector embeddings from the configured Qdrant collection.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from qdrant_client.models import Filter, FieldCondition, MatchValue

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "actowiz_embeddings"

# Shared Qdrant client instance
client = QdrantClient(url=QDRANT_URL)


def create_collection():

    collections = client.get_collections()
    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def store_embedding(
    point_id: str,
    embedding: list[float],
    payload: dict,
) -> None:
    """
    Store an embedding vector in Qdrant.

    Args:
        point_id: Unique identifier for the vector.
        embedding: Vector representation of the content.
        payload: Metadata associated with the vector.
    """
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            )
        ],
    )


def search_document(query_vector, limit=5, metadata_filters=None):

    query_filter = None

    if metadata_filters:

        conditions = []
        for key, value in metadata_filters.items():

            conditions.append(
                FieldCondition(
                    key=key,
                    match=MatchValue(value=value)
                )
            )

        query_filter = Filter(
            must=conditions
        )

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=query_filter,
        limit=limit
    )

    return results


# Delete Document Embeddings
def delete_document_embeddings(document_id):

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id)
                )
            ]
        )
    )