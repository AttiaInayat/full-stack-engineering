from fastapi import APIRouter

from production.app.schemas.chat import ChatRequest, ChatResponse
from production.app.services.chat_service import chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    answer = chat(request.message)
    return ChatResponse(answer=answer)

