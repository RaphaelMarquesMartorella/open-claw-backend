'''Service de relatorios do agente.'''
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import save_report_repository, get_reports_repository


async def save_report_service(
    db: AsyncSession,
    agent_name: str,
    report_text: str,
    score: int | None = None,
    status: str = 'generated',
    whatsapp_sent: str = 'N'
) -> int:
    '''Salva relatorio e retorna o ID.'''
    return await save_report_repository(
        db, agent_name, report_text, score, status, whatsapp_sent
    )


async def get_reports_service(db: AsyncSession, limit: int = 20) -> dict:
    '''Retorna lista de relatorios.'''
    reports = await get_reports_repository(db, limit)
    return {'reports': reports}
