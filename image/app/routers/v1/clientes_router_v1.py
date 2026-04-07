'''Router de endpoints de clientes inativos.'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_db
from schemas import ClienteInativoResponse
from services import get_clientes_inativos_service

clientes_router = APIRouter()


@clientes_router.get(
    '/inativos',
    response_model=ClienteInativoResponse,
    description='Clientes que compraram no mes anterior mas sumiram no atual',
    summary='Clientes inativos',
    status_code=status.HTTP_200_OK,
)
async def get_clientes_inativos(db: AsyncSession = Depends(get_db)):
    return await get_clientes_inativos_service(db)
