from fastapi import APIRouter
from controllers.gateway_controller import chat

router = APIRouter()


@router.post("/chat")
async def gateway_chat(payload: dict):
    """
    Centralized AI Gateway endpoint.
    Routes requests to configured LLM providers.
    """
    return await chat(payload)
