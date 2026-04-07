'''Router de endpoints de relatorios.'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import ReportListResponse
from services import get_reports_service

reports_router = APIRouter()


@reports_router.get(
    '/',
    response_model=ReportListResponse,
    description='Lista ultimos relatorios gerados pelo agente',
    summary='Listar relatorios',
    status_code=status.HTTP_200_OK,
)
async def get_reports(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    return await get_reports_service(db, limit)
