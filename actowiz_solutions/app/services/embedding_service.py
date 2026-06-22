"""
Embedding generation service.
"""

from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    """
    Generate a vector embedding for the provided text.
    """
    print("Generating embedding...")
    return model.encode(text).tolist()
