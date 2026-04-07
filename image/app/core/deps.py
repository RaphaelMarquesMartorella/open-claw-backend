import logging
from .database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    '''Injecao de dependencia para sessao do banco de dados.'''
    try:
        async with SessionLocal() as session:
            yield session
    except Exception as e:
        logging.error(f'Erro de conexao: {e}')
        raise e
