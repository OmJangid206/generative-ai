import os

from openai import OpenAI
from fastapi import HTTPException
from dotenv import load_dotenv

from services.embedding_service import generate_embedding
from db.qdrant_service import search_document


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPEN_ROUTER_API"]
)


async def chat(payload: dict):

    try:

        query = payload.get("query")
        provider = payload.get(
            "provider",
            "openai/gpt-4o-mini"
        )

        if not query:
            raise HTTPException(
                status_code=400,
                detail="Query is required"
            )

        query_vector = generate_embedding(query)

        results = search_document(
            query_vector=query_vector,
            limit=5
        )

        context = "\n".join([
            item.payload.get("content", "")
            for item in results
        ])

        prompt = f"""
            Context:
            {context}

            Question:
            {query}

            Answer using only the provided context.
        """

        response = client.chat.completions.create(
            model=provider,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "provider": provider,
            "query": query,
            "response": response.choices[0].message.content
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )