'''Router de endpoints do agente.'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import AgentTriggerResponse
from services import run_agent_service

agente_router = APIRouter()


@agente_router.post(
    '/trigger',
    response_model=AgentTriggerResponse,
    description='Dispara o agente gestor comercial manualmente',
    summary='Disparar agente',
    status_code=status.HTTP_200_OK,
)
async def trigger_agent(db: AsyncSession = Depends(get_db)):
    result = await run_agent_service(db)
    return {
        'status': result['status'],
        'message': result['message'],
        'report_id': result.get('report_id'),
    }
