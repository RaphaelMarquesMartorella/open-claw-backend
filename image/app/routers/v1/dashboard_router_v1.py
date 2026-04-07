'''Router de endpoints do dashboard.'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import KPIResponse, ComparativoDiarioResponse
from services import get_kpis_service, get_comparativo_diario_service

dashboard_router = APIRouter()


@dashboard_router.get(
    '/kpis',
    response_model=KPIResponse,
    description='KPIs comparativos mes atual vs anterior',
    summary='KPIs do dashboard',
    status_code=status.HTTP_200_OK,
)
async def get_kpis(db: AsyncSession = Depends(get_db)):
    return await get_kpis_service(db)


@dashboard_router.get(
    '/comparativo-diario',
    response_model=ComparativoDiarioResponse,
    description='Faturamento diario dos ultimos 30 dias',
    summary='Comparativo diario',
    status_code=status.HTTP_200_OK,
)
async def get_comparativo_diario(
    dias: int = 30,
    db: AsyncSession = Depends(get_db),
):
    return await get_comparativo_diario_service(db, dias)
