'''Router do chatbot WhatsApp.'''
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from services.chat_service import chat_service

chat_router = APIRouter()


class ChatRequest(BaseModel):
    sender: str = Field(..., description='Identificador do remetente (ex: 5581999999999@c.us)')
    text: str = Field(..., min_length=1, description='Texto da mensagem recebida')


class ChatResponse(BaseModel):
    reply: str


@chat_router.post(
    '/message',
    response_model=ChatResponse,
    description='Processa mensagem recebida e retorna resposta do agente',
    summary='Chat WhatsApp',
    status_code=status.HTTP_200_OK,
)
async def chat_message(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    reply = await chat_service(db, payload.sender, payload.text)
    return {'reply': reply}
