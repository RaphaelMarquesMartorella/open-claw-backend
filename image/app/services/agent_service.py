'''
Service do Agente Gestor Comercial de Elite.
Coleta dados, gera relatorio via LLM e envia via WhatsApp.
'''
import json
import logging
import re
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings
from repositories import (
    get_kpis_repository,
    get_vendedor_ranking_repository,
    get_top_produtos_repository,
    get_clientes_inativos_repository,
)
from .report_service import save_report_service
from .whatsapp_service import send_whatsapp_report_service

logger = logging.getLogger('AGENT.GESTOR_COMERCIAL')

SYSTEM_PROMPT = '''Voce e um Gestor Comercial de Elite com 20 anos de experiencia em distribuidoras \
de alto desempenho. Seu papel e analisar os dados de vendas comparativos entre o \
mes atual e o mes anterior, identificar desvios criticos de performance e emitir \
um relatorio executivo diretamente no WhatsApp do diretor.
Sua analise DEVE conter obrigatoriamente:

RANKING DE VENDEDORES: Compare faturamento atual vs. mes anterior por vendedor. \
Destaque os top 3 e os bottom 3. Seja direto e sem rodeios.
ALERTAS CRITICOS: Identifique vendedores com queda > 10% e clientes que \
pararam de comprar (compraram no mes anterior mas nao no atual).
ANALISE DE PRODUTOS: Top 10 produtos por faturamento. Identifique produtos \
com estoque alto e baixa saida.
RECOMENDACOES ATIVAS: Para cada alerta, emita uma acao concreta. \
Ex: "Acionar vendedor X para visitar cliente Y que comprou R$50k no mes passado \
e nao fez nenhum pedido este mes."
SCORE GERAL DO MES: De uma nota de 0 a 10 para a performance comercial \
do periodo com justificativa.

Seu tom e direto, executivo, sem enrolacao. Voce cobra resultados.
Formate o relatorio para leitura facil no WhatsApp (use emojis estrategicos, \
quebras de linha, e secoes bem delimitadas). Limite: 4000 caracteres.'''


async def _collect_data(db: AsyncSession) -> str:
    '''Coleta todos os dados necessarios para o agente.'''
    kpis = await get_kpis_repository(db)
    ranking = await get_vendedor_ranking_repository(db)
    produtos = await get_top_produtos_repository(db, limit=10)
    inativos = await get_clientes_inativos_repository(db)

    data = {
        'kpis': kpis,
        'ranking_vendedores': ranking,
        'top_produtos': produtos,
        'clientes_inativos': inativos,
    }

    return json.dumps(data, ensure_ascii=False, default=str)


def _extract_score(report_text: str) -> int | None:
    '''Extrai o score numerico do relatorio gerado.'''
    patterns = [
        r'(?:SCORE|NOTA|score|nota)[^\d]*(\d+(?:[.,]\d+)?)\s*/?\s*10',
        r'(\d+(?:[.,]\d+)?)\s*/\s*10',
    ]
    for pattern in patterns:
        match = re.search(pattern, report_text)
        if match:
            try:
                score = float(match.group(1).replace(',', '.'))
                return min(int(round(score)), 10)
            except ValueError:
                continue
    return None


async def run_agent_service(db: AsyncSession) -> dict:
    '''Executa o agente Gestor Comercial completo.'''
    logger.info('Iniciando execucao do Agente Gestor Comercial...')

    # 1. Coletar dados
    logger.info('Coletando dados do banco...')
    data_json = await _collect_data(db)
    logger.info(f'Dados coletados: {len(data_json)} caracteres')

    # 2. Gerar relatorio via LLM
    logger.info('Gerando relatorio via LLM...')
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        response = await client.chat.completions.create(
            model='gpt-5.4',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': f'Analise os seguintes dados e gere o relatorio:\n\n{data_json}'},
            ],
            max_tokens=2000,
            temperature=0.7,
        )
        report_text = response.choices[0].message.content
        logger.info('Relatorio gerado com sucesso')
    except Exception as ex:
        logger.error(f'Erro ao gerar relatorio via LLM: {ex}')
        # Fallback: gerar relatorio simples sem LLM
        report_text = await _generate_fallback_report(db)
        logger.info('Relatorio fallback gerado')

    # 3. Extrair score
    score = _extract_score(report_text)
    logger.info(f'Score extraido: {score}')

    # 4. Enviar via WhatsApp
    logger.info('Enviando relatorio via WhatsApp...')
    wpp_result = send_whatsapp_report_service(report_text)
    # Handle both sync and async
    if hasattr(wpp_result, '__await__'):
        wpp_result = await wpp_result

    whatsapp_sent = 'S' if wpp_result.get('status') == 'sent' else 'N'

    # 5. Salvar relatorio no banco
    status = 'sent' if whatsapp_sent == 'S' else 'generated'
    report_id = await save_report_service(
        db, 'gestor_comercial', report_text, score, status, whatsapp_sent
    )
    logger.info(f'Relatorio salvo com ID: {report_id}')

    return {
        'status': 'ok',
        'message': 'Agente executado com sucesso',
        'report_id': report_id,
        'score': score,
        'whatsapp_status': wpp_result.get('status'),
        'report_preview': report_text[:500],
    }


async def _generate_fallback_report(db: AsyncSession) -> str:
    '''Gera relatorio simples sem LLM (fallback).'''
    kpis = await get_kpis_repository(db)
    ranking = await get_vendedor_ranking_repository(db)
    inativos = await get_clientes_inativos_repository(db)
    produtos = await get_top_produtos_repository(db, 10)

    # Top 3 e Bottom 3
    top3 = ranking[:3] if len(ranking) >= 3 else ranking
    bottom3 = ranking[-3:] if len(ranking) >= 3 else ranking

    # Vendedores em queda
    em_queda = [v for v in ranking if v['delta_percentual'] < -10]

    lines = []
    lines.append('📊 *RELATORIO COMERCIAL - GESTOR DE ELITE*')
    lines.append('=' * 40)
    lines.append('')
    lines.append(f'💰 *Faturamento Atual:* R$ {kpis["faturamento_atual"]:,.2f}')
    lines.append(f'📈 *Faturamento Anterior:* R$ {kpis["faturamento_anterior"]:,.2f}')
    lines.append(f'📉 *Delta:* {kpis["delta_percentual"]:+.1f}%')
    lines.append('')

    lines.append('🏆 *TOP 3 VENDEDORES:*')
    for v in top3:
        emoji = '🟢' if v['delta_percentual'] >= 0 else '🔴'
        lines.append(f'{emoji} {v["apelido"]}: R$ {v["fat_atual"]:,.2f} ({v["delta_percentual"]:+.1f}%)')

    lines.append('')
    lines.append('⚠️ *BOTTOM 3 VENDEDORES:*')
    for v in bottom3:
        emoji = '🟢' if v['delta_percentual'] >= 0 else '🔴'
        lines.append(f'{emoji} {v["apelido"]}: R$ {v["fat_atual"]:,.2f} ({v["delta_percentual"]:+.1f}%)')

    if em_queda:
        lines.append('')
        lines.append('🚨 *ALERTAS - QUEDA > 10%:*')
        for v in em_queda:
            lines.append(f'❌ {v["apelido"]}: {v["delta_percentual"]:+.1f}%')

    if inativos:
        lines.append('')
        lines.append(f'👻 *CLIENTES INATIVOS: {len(inativos)}*')
        valor_risco = sum(c['valor_anterior'] for c in inativos)
        lines.append(f'💸 Valor em risco: R$ {valor_risco:,.2f}')
        for c in inativos[:5]:
            lines.append(f'  • {c["nomeparc"]} ({c["cidade"]}/{c["uf"]}) - R$ {c["valor_anterior"]:,.2f}')

    lines.append('')
    lines.append('📦 *TOP 5 PRODUTOS:*')
    for p in produtos[:5]:
        lines.append(f'  • {p["descrprod"]}: R$ {p["faturamento"]:,.2f}')

    # Score simples baseado no delta
    delta = kpis['delta_percentual']
    if delta >= 10:
        score = 9
    elif delta >= 0:
        score = 7
    elif delta >= -10:
        score = 5
    elif delta >= -20:
        score = 3
    else:
        score = 1

    lines.append('')
    lines.append(f'⭐ *SCORE DO MES: {score}/10*')
    lines.append('')
    lines.append('_Relatorio gerado automaticamente pelo OpenClaw_')

    return '\n'.join(lines)
