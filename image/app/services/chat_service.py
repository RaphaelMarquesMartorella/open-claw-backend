'''Chatbot WhatsApp - Gestor Comercial interativo com tool-calling.'''
import json
import logging
from collections import defaultdict, deque
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings
from repositories import (
    get_kpis_repository,
    get_vendedor_ranking_repository,
    get_top_produtos_repository,
    get_clientes_inativos_repository,
    get_comparativo_diario_repository,
    get_vendedor_detalhe_repository,
)

logger = logging.getLogger('AGENT.CHAT')

MODEL = 'gpt-5.4'
MAX_HISTORY_TURNS = 8
MAX_TOOL_ITERATIONS = 5

SYSTEM_PROMPT = '''Voce e o Gestor Comercial de Elite da Pneubras — um consultor com 20 anos de \
experiencia em distribuidoras de pneus. Voce responde perguntas do diretor via WhatsApp usando \
as ferramentas disponiveis para consultar dados reais de vendas.

REGRAS:
1. Sempre use as ferramentas para buscar dados — nunca invente numeros.
2. Seja direto, executivo, sem rodeios. Respostas curtas (WhatsApp).
3. Use emojis estrategicos (🟢 🔴 📈 📉 ⚠️ 💰 🏆) mas sem exagero.
4. Formate valores como R$ 1.234,56 e percentuais como +12,3% / -5,1%.
5. Quando listar vendedores/produtos/clientes, maximo 5-10 itens por resposta.
6. Se a pergunta for ambigua, pergunte de volta em vez de chutar.
7. Se a pergunta nao for sobre vendas/negocio, responda brevemente que voce e o assistente \
comercial e lista o que sabe fazer.'''

TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_kpis',
            'description': 'Retorna KPIs gerais: faturamento atual vs anterior, delta percentual, total de pedidos e clientes ativos.',
            'parameters': {'type': 'object', 'properties': {}, 'required': []},
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_vendedor_ranking',
            'description': 'Ranking completo de vendedores com faturamento atual, anterior e delta percentual. Use quando perguntarem sobre performance de vendedores, top/bottom, quedas.',
            'parameters': {'type': 'object', 'properties': {}, 'required': []},
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_top_produtos',
            'description': 'Top produtos por faturamento no mes corrente. Inclui qtd, estoque e giro.',
            'parameters': {
                'type': 'object',
                'properties': {'limit': {'type': 'integer', 'description': 'Quantos produtos retornar (1-50).', 'default': 10}},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_clientes_inativos',
            'description': 'Clientes que compraram no mes anterior mas nao no atual. Retorna lista e valor em risco.',
            'parameters': {'type': 'object', 'properties': {}, 'required': []},
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_comparativo_diario',
            'description': 'Faturamento dia a dia nos ultimos N dias.',
            'parameters': {
                'type': 'object',
                'properties': {'dias': {'type': 'integer', 'description': 'Quantos dias (1-90).', 'default': 30}},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_vendedor_detalhe',
            'description': 'Detalhe de um vendedor especifico pelo codigo. Use apos get_vendedor_ranking para pegar o codvend.',
            'parameters': {
                'type': 'object',
                'properties': {'codvend': {'type': 'integer', 'description': 'Codigo do vendedor.'}},
                'required': ['codvend'],
            },
        },
    },
]


_history: dict[str, deque] = defaultdict(lambda: deque(maxlen=MAX_HISTORY_TURNS * 2))


async def _run_tool(db: AsyncSession, name: str, args: dict) -> str:
    '''Executa a ferramenta solicitada e retorna JSON string.'''
    try:
        if name == 'get_kpis':
            data = await get_kpis_repository(db)
        elif name == 'get_vendedor_ranking':
            data = await get_vendedor_ranking_repository(db)
        elif name == 'get_top_produtos':
            limit = int(args.get('limit', 10))
            data = await get_top_produtos_repository(db, max(1, min(limit, 50)))
        elif name == 'get_clientes_inativos':
            data = await get_clientes_inativos_repository(db)
        elif name == 'get_comparativo_diario':
            dias = int(args.get('dias', 30))
            data = await get_comparativo_diario_repository(db, max(1, min(dias, 90)))
        elif name == 'get_vendedor_detalhe':
            data = await get_vendedor_detalhe_repository(db, int(args['codvend']))
        else:
            data = {'error': f'ferramenta desconhecida: {name}'}
        return json.dumps(data, ensure_ascii=False, default=str)
    except Exception as ex:
        logger.error(f'Erro executando tool {name}: {ex}', exc_info=True)
        return json.dumps({'error': str(ex)})


async def chat_service(db: AsyncSession, sender: str, text: str) -> str:
    '''Processa uma mensagem e retorna a resposta do agente.'''
    history = _history[sender]
    history.append({'role': 'user', 'content': text})

    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + list(history)

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    for _ in range(MAX_TOOL_ITERATIONS):
        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            max_completion_tokens=1500,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            reply = (msg.content or '').strip() or 'Nao consegui gerar resposta.'
            history.append({'role': 'assistant', 'content': reply})
            return reply

        messages.append({
            'role': 'assistant',
            'content': msg.content,
            'tool_calls': [
                {'id': tc.id, 'type': 'function', 'function': {'name': tc.function.name, 'arguments': tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        for tc in msg.tool_calls:
            try:
                args = json.loads(tc.function.arguments or '{}')
            except json.JSONDecodeError:
                args = {}
            logger.info(f'[{sender}] tool={tc.function.name} args={args}')
            result = await _run_tool(db, tc.function.name, args)
            messages.append({'role': 'tool', 'tool_call_id': tc.id, 'content': result})

    fallback = 'Nao consegui completar a analise. Tenta reformular a pergunta.'
    history.append({'role': 'assistant', 'content': fallback})
    return fallback
