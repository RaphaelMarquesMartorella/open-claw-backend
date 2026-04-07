'''
OpenClaw - API do Agente Gestor Comercial
Ponto de entrada da aplicacao FastAPI.
'''
import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.configs import settings
from core.logger import setup_logging
from core.database import SessionLocal, engine
from core.configs import settings as cfg
from routers import dsh, vnd, prd, cli, agt, rpt

# Configurar logging
setup_logging()
logger = logging.getLogger('MAIN')

# Scheduler
scheduler = AsyncIOScheduler()


async def _scheduled_agent_run():
    '''Tarefa agendada: executa o agente gestor comercial.'''
    from services import run_agent_service
    logger.info('Executando agente agendado...')
    try:
        async with SessionLocal() as db:
            result = await run_agent_service(db)
            logger.info(f'Agente concluido: {result.get("message")}')
    except Exception as ex:
        logger.error(f'Erro na execucao agendada: {ex}', exc_info=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Ciclo de vida da aplicacao.'''
    logger.info(f'OpenClaw API v{settings.API_VERSION} iniciando...')

    # Criar tabela de relatorios se nao existir
    from sqlalchemy import text
    async with engine.begin() as conn:
        await conn.execute(text('''
            CREATE TABLE IF NOT EXISTS agent_reports (
                id SERIAL PRIMARY KEY,
                agent_name VARCHAR(100) NOT NULL,
                report_text TEXT NOT NULL,
                score INTEGER,
                status VARCHAR(20) DEFAULT 'generated',
                whatsapp_sent CHAR(1) DEFAULT 'N',
                created_at TIMESTAMP DEFAULT NOW()
            )
        '''))

    # Configurar agendamento
    hour, minute = cfg.AGENT_SCHEDULE.split(':')
    tz = timezone(cfg.AGENT_TIMEZONE)
    scheduler.add_job(
        _scheduled_agent_run,
        CronTrigger(hour=int(hour), minute=int(minute), timezone=tz),
        id='gestor_comercial_daily',
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f'Agendamento configurado: {cfg.AGENT_SCHEDULE} ({cfg.AGENT_TIMEZONE})')

    yield

    scheduler.shutdown()
    logger.info('OpenClaw API encerrada.')


app = FastAPI(
    title='OpenClaw - Agente Gestor Comercial',
    version=settings.API_VERSION,
    description='API do agente gestor comercial inteligente para distribuidoras.',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Registrar routers
app.include_router(dsh, prefix='/api/v1/dashboard', tags=['Dashboard'])
app.include_router(vnd, prefix='/api/v1/vendedores', tags=['Vendedores'])
app.include_router(prd, prefix='/api/v1/produtos', tags=['Produtos'])
app.include_router(cli, prefix='/api/v1/clientes', tags=['Clientes'])
app.include_router(agt, prefix='/api/v1/agente', tags=['Agente'])
app.include_router(rpt, prefix='/api/v1/relatorios', tags=['Relatorios'])


@app.get('/api/health')
async def health():
    return {'status': 'ok', 'version': settings.API_VERSION, 'agent': 'gestor_comercial'}


# CLI: python main.py --agent gestor_comercial --run-now
if __name__ == '__main__':
    if '--run-now' in sys.argv:
        async def _run_now():
            setup_logging()
            logger.info('Execucao manual do agente...')
            from services import run_agent_service
            # Criar tabela se nao existir
            from sqlalchemy import text as sa_text
            async with engine.begin() as conn:
                await conn.execute(sa_text('''
                    CREATE TABLE IF NOT EXISTS agent_reports (
                        id SERIAL PRIMARY KEY,
                        agent_name VARCHAR(100) NOT NULL,
                        report_text TEXT NOT NULL,
                        score INTEGER,
                        status VARCHAR(20) DEFAULT 'generated',
                        whatsapp_sent CHAR(1) DEFAULT 'N',
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                '''))
            async with SessionLocal() as db:
                result = await run_agent_service(db)
            print('\n' + '=' * 60)
            print('RESULTADO DO AGENTE:')
            print('=' * 60)
            print(f'Status: {result["status"]}')
            print(f'Report ID: {result.get("report_id")}')
            print(f'Score: {result.get("score")}')
            print(f'WhatsApp: {result.get("whatsapp_status")}')
            print('=' * 60)
            print('RELATORIO:')
            print('=' * 60)
            # Buscar relatorio completo
            from repositories import get_reports_repository
            async with SessionLocal() as db:
                reports = await get_reports_repository(db, 1)
            if reports:
                print(reports[0]['report_text'])
            print('=' * 60)

        asyncio.run(_run_now())
    else:
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=8000)
