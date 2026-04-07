'''Service de dados do dashboard.'''
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import (
    get_kpis_repository,
    get_vendedor_ranking_repository,
    get_top_produtos_repository,
    get_clientes_inativos_repository,
    get_comparativo_diario_repository,
    get_vendedor_detalhe_repository,
)


async def get_kpis_service(db: AsyncSession) -> dict:
    '''Retorna KPIs do dashboard.'''
    return await get_kpis_repository(db)


async def get_vendedor_ranking_service(db: AsyncSession) -> dict:
    '''Retorna ranking de vendedores.'''
    vendedores = await get_vendedor_ranking_repository(db)
    return {'vendedores': vendedores}


async def get_top_produtos_service(db: AsyncSession, limit: int = 10) -> dict:
    '''Retorna top produtos por faturamento.'''
    produtos = await get_top_produtos_repository(db, limit)
    return {'produtos': produtos}


async def get_clientes_inativos_service(db: AsyncSession) -> dict:
    '''Retorna clientes inativos com valor em risco.'''
    clientes = await get_clientes_inativos_repository(db)
    valor_total = sum(c['valor_anterior'] for c in clientes)
    return {'clientes': clientes, 'valor_total_risco': round(valor_total, 2)}


async def get_comparativo_diario_service(db: AsyncSession, dias: int = 30) -> dict:
    '''Retorna comparativo diario.'''
    dias_data = await get_comparativo_diario_repository(db, dias)
    return {'dias': dias_data}


async def get_vendedor_detalhe_service(db: AsyncSession, codvend: int) -> dict | None:
    '''Retorna detalhe de vendedor.'''
    return await get_vendedor_detalhe_repository(db, codvend)
