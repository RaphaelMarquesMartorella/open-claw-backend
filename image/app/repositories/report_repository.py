'''Repositorio para relatorios do agente.'''
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def save_report_repository(
    db: AsyncSession,
    agent_name: str,
    report_text: str,
    score: int | None,
    status: str = 'generated',
    whatsapp_sent: str = 'N'
) -> int:
    '''Salva um relatorio gerado pelo agente. Retorna o ID.'''
    query = text('''
        INSERT INTO agent_reports (agent_name, report_text, score, status, whatsapp_sent, created_at)
        VALUES (:agent_name, :report_text, :score, :status, :whatsapp_sent, NOW())
        RETURNING id
    ''')
    result = await db.execute(query, {
        'agent_name': agent_name,
        'report_text': report_text,
        'score': score,
        'status': status,
        'whatsapp_sent': whatsapp_sent,
    })
    await db.commit()
    return result.scalar()


async def get_reports_repository(db: AsyncSession, limit: int = 20) -> list[dict]:
    '''Retorna os ultimos relatorios gerados.'''
    query = text('''
        SELECT id, agent_name, report_text, score, status, whatsapp_sent, created_at
        FROM agent_reports
        ORDER BY created_at DESC
        LIMIT :limit
    ''')
    result = await db.execute(query, {'limit': limit})
    rows = result.fetchall()
    return [
        {
            'id': row[0],
            'agent_name': row[1],
            'report_text': row[2],
            'score': row[3],
            'status': row[4],
            'whatsapp_sent': row[5],
            'created_at': row[6],
        }
        for row in rows
    ]
