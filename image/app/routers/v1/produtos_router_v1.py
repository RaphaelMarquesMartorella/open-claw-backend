'''Router de endpoints de produtos.'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import ProdutoRankingResponse
from services import get_top_produtos_service

produtos_router = APIRouter()


@produtos_router.get(
    '/',
    response_model=ProdutoRankingResponse,
    description='Top produtos por faturamento',
    summary='Ranking de produtos',
    status_code=status.HTTP_200_OK,
)
async def get_produtos(
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await get_top_produtos_service(db, limit)
