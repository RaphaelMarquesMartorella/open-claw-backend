'''Router de endpoints de vendedores.'''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import VendedorRankingResponse, VendedorDetalheResponse
from services import get_vendedor_ranking_service, get_vendedor_detalhe_service

vendedores_router = APIRouter()


@vendedores_router.get(
    '/',
    response_model=VendedorRankingResponse,
    description='Ranking completo de vendedores com delta percentual',
    summary='Ranking de vendedores',
    status_code=status.HTTP_200_OK,
)
async def get_vendedores(db: AsyncSession = Depends(get_db)):
    return await get_vendedor_ranking_service(db)


@vendedores_router.get(
    '/{codvend}',
    response_model=VendedorDetalheResponse,
    description='Detalhe de vendedor com breakdown por cliente e produto',
    summary='Detalhe de vendedor',
    status_code=status.HTTP_200_OK,
)
async def get_vendedor_detalhe(
    codvend: int,
    db: AsyncSession = Depends(get_db),
):
    result = await get_vendedor_detalhe_service(db, codvend)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vendedor nao encontrado')
    return result
