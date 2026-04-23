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


class ChatAttachment(BaseModel):
    filename: str
    mime_type: str
    data_base64: str


class ChatResponse(BaseModel):
    reply: str
    attachments: list[ChatAttachment] = []


@chat_router.post(
    '/message',
    response_model=ChatResponse,
    description='Processa mensagem recebida e retorna resposta do agente',
    summary='Chat WhatsApp',
    status_code=status.HTTP_200_OK,
)
async def chat_message(payload: ChatRequest, db: AsyncSession = Depends(get_db)):
    reply, attachments = await chat_service(db, payload.sender, payload.text)
    return {
        'reply': reply,
        'attachments': [
            {'filename': a['filename'], 'mime_type': a['mime_type'], 'data_base64': a['data_base64']}
            for a in attachments
        ],
    }
