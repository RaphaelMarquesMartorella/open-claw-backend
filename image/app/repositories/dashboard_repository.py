'''Repositorio de queries do dashboard e tools do agente.'''
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_kpis_repository(db: AsyncSession) -> dict:
    '''Retorna KPIs comparativos mes atual vs anterior.'''
    query = text('''
        WITH mes_atual AS (
            SELECT
                COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento,
                COUNT(DISTINCT c."NUNOTA") AS total_pedidos,
                COUNT(DISTINCT c."CODPARC") AS clientes_ativos
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
        ),
        mes_anterior AS (
            SELECT
                COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento,
                COUNT(DISTINCT c."NUNOTA") AS total_pedidos
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
              AND c."DTNEG" < date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
        )
        SELECT
            ma.faturamento AS fat_atual,
            me.faturamento AS fat_anterior,
            CASE WHEN me.faturamento > 0
                THEN ROUND(((ma.faturamento - me.faturamento) / me.faturamento * 100)::numeric, 2)
                ELSE 0 END AS delta_pct,
            ma.clientes_ativos,
            ma.total_pedidos AS pedidos_atual,
            me.total_pedidos AS pedidos_anterior,
            CASE WHEN ma.total_pedidos > 0
                THEN ROUND((ma.faturamento / ma.total_pedidos)::numeric, 2)
                ELSE 0 END AS ticket_atual,
            CASE WHEN me.total_pedidos > 0
                THEN ROUND((me.faturamento / me.total_pedidos)::numeric, 2)
                ELSE 0 END AS ticket_anterior
        FROM mes_atual ma, mes_anterior me
    ''')
    result = await db.execute(query)
    row = result.fetchone()
    return {
        'faturamento_atual': float(row[0]),
        'faturamento_anterior': float(row[1]),
        'delta_percentual': float(row[2]),
        'clientes_ativos': int(row[3]),
        'total_pedidos_atual': int(row[4]),
        'total_pedidos_anterior': int(row[5]),
        'ticket_medio_atual': float(row[6]),
        'ticket_medio_anterior': float(row[7]),
    }


async def get_vendedor_ranking_repository(db: AsyncSession) -> list[dict]:
    '''Ranking de vendedores com comparativo mensal.'''
    query = text('''
        WITH fat_atual AS (
            SELECT c."CODVEND",
                   COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento,
                   COUNT(DISTINCT c."NUNOTA") AS pedidos
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
            GROUP BY c."CODVEND"
        ),
        fat_anterior AS (
            SELECT c."CODVEND",
                   COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento,
                   COUNT(DISTINCT c."NUNOTA") AS pedidos
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
              AND c."DTNEG" < date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
            GROUP BY c."CODVEND"
        )
        SELECT
            v."CODVEND",
            v."APELIDO",
            v."NOMEVEND",
            COALESCE(fa.faturamento, 0) AS fat_atual,
            COALESCE(fp.faturamento, 0) AS fat_anterior,
            CASE WHEN COALESCE(fp.faturamento, 0) > 0
                THEN ROUND(((COALESCE(fa.faturamento, 0) - fp.faturamento) / fp.faturamento * 100)::numeric, 2)
                ELSE 0 END AS delta_pct,
            COALESCE(fa.pedidos, 0) AS pedidos_atual,
            COALESCE(fp.pedidos, 0) AS pedidos_anterior
        FROM "TGFVEND" v
        LEFT JOIN fat_atual fa ON v."CODVEND" = fa."CODVEND"
        LEFT JOIN fat_anterior fp ON v."CODVEND" = fp."CODVEND"
        WHERE v."ATIVO" = 'S'
        ORDER BY fat_atual DESC
    ''')
    result = await db.execute(query)
    rows = result.fetchall()
    return [
        {
            'codvend': row[0],
            'apelido': row[1],
            'nomevend': row[2],
            'fat_atual': float(row[3]),
            'fat_anterior': float(row[4]),
            'delta_percentual': float(row[5]),
            'qtd_pedidos_atual': int(row[6]),
            'qtd_pedidos_anterior': int(row[7]),
        }
        for row in rows
    ]


async def get_top_produtos_repository(db: AsyncSession, limit: int = 10) -> list[dict]:
    '''Top produtos por faturamento no periodo (mes anterior + mes atual).'''
    query = text('''
        WITH vendas AS (
            SELECT i."CODPROD",
                   SUM(i."VLRTOT") AS faturamento,
                   SUM(i."QTDNEG") AS qtd_vendida
            FROM "TGFITE" i
            JOIN "TGFCAB" c ON i."NUNOTA" = c."NUNOTA"
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
              AND c."STATUSNOTA" = 'L'
            GROUP BY i."CODPROD"
        )
        SELECT
            p."CODPROD",
            p."DESCRPROD",
            p."MARCA",
            COALESCE(v.qtd_vendida, 0) AS qtd_vendida,
            COALESCE(v.faturamento, 0) AS faturamento,
            p."ESTOQUE",
            CASE WHEN p."ESTOQUE" > 0 AND COALESCE(v.qtd_vendida, 0) > 0
                THEN ROUND((p."ESTOQUE" / v.qtd_vendida)::numeric, 2)
                ELSE 0 END AS giro
        FROM "TGFPRO" p
        LEFT JOIN vendas v ON p."CODPROD" = v."CODPROD"
        WHERE p."ATIVO" = 'S'
        ORDER BY faturamento DESC
        LIMIT :limit
    ''')
    result = await db.execute(query, {'limit': limit})
    rows = result.fetchall()
    return [
        {
            'codprod': row[0],
            'descrprod': row[1],
            'marca': row[2],
            'qtd_vendida': float(row[3]),
            'faturamento': float(row[4]),
            'estoque': float(row[5]),
            'giro': float(row[6]),
        }
        for row in rows
    ]


async def get_clientes_inativos_repository(db: AsyncSession) -> list[dict]:
    '''Clientes que compraram no mes anterior mas nao no atual.'''
    query = text('''
        WITH compras_anterior AS (
            SELECT
                c."CODPARC",
                SUM(c."VLRNOTA") AS valor_anterior,
                MAX(c."DTNEG") AS ultimo_pedido,
                (SELECT v."APELIDO" FROM "TGFVEND" v WHERE v."CODVEND" = MAX(c."CODVEND")) AS vendedor
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
              AND c."DTNEG" < date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
            GROUP BY c."CODPARC"
        ),
        compras_atual AS (
            SELECT DISTINCT c."CODPARC"
            FROM "TGFCAB" c
            WHERE c."DTNEG" >= date_trunc('month', CURRENT_DATE)
              AND c."STATUSNOTA" = 'L'
        )
        SELECT
            p."CODPARC",
            p."NOMEPARC",
            p."CIDADE",
            p."UF",
            ca.valor_anterior,
            TO_CHAR(ca.ultimo_pedido, 'DD/MM/YYYY') AS ultimo_pedido,
            ca.vendedor
        FROM compras_anterior ca
        JOIN "TGFPAR" p ON ca."CODPARC" = p."CODPARC"
        LEFT JOIN compras_atual cc ON ca."CODPARC" = cc."CODPARC"
        WHERE cc."CODPARC" IS NULL
        ORDER BY ca.valor_anterior DESC
    ''')
    result = await db.execute(query)
    rows = result.fetchall()
    return [
        {
            'codparc': row[0],
            'nomeparc': row[1],
            'cidade': row[2],
            'uf': row[3],
            'valor_anterior': float(row[4]),
            'ultimo_pedido': row[5],
            'vendedor_responsavel': row[6],
        }
        for row in rows
    ]


async def get_comparativo_diario_repository(db: AsyncSession, dias: int = 30) -> list[dict]:
    '''Faturamento diario dos ultimos N dias.'''
    query = text('''
        SELECT
            TO_CHAR(c."DTNEG"::date, 'YYYY-MM-DD') AS data,
            COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento
        FROM "TGFCAB" c
        WHERE c."DTNEG" >= CURRENT_DATE - make_interval(days => :dias)
          AND c."STATUSNOTA" = 'L'
        GROUP BY c."DTNEG"::date
        ORDER BY c."DTNEG"::date
    ''')
    result = await db.execute(query, {'dias': dias})
    rows = result.fetchall()
    return [
        {
            'data': row[0],
            'faturamento': float(row[1]),
        }
        for row in rows
    ]


async def get_vendedor_detalhe_repository(db: AsyncSession, codvend: int) -> dict:
    '''Detalhe de um vendedor com breakdown por cliente e produto.'''
    # Info do vendedor
    vend_query = text('''
        SELECT v."CODVEND", v."APELIDO", v."NOMEVEND"
        FROM "TGFVEND" v WHERE v."CODVEND" = :codvend
    ''')
    vend_result = await db.execute(vend_query, {'codvend': codvend})
    vend = vend_result.fetchone()
    if not vend:
        return None

    # Faturamento atual e anterior
    fat_query = text('''
        SELECT
            COALESCE(SUM(CASE WHEN c."DTNEG" >= date_trunc('month', CURRENT_DATE)
                THEN c."VLRNOTA" ELSE 0 END), 0) AS fat_atual,
            COALESCE(SUM(CASE WHEN c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
                AND c."DTNEG" < date_trunc('month', CURRENT_DATE)
                THEN c."VLRNOTA" ELSE 0 END), 0) AS fat_anterior
        FROM "TGFCAB" c
        WHERE c."CODVEND" = :codvend AND c."STATUSNOTA" = 'L'
    ''')
    fat_result = await db.execute(fat_query, {'codvend': codvend})
    fat = fat_result.fetchone()

    # Clientes do vendedor
    cli_query = text('''
        SELECT p."CODPARC", p."NOMEPARC",
            COALESCE(SUM(c."VLRNOTA"), 0) AS faturamento,
            COUNT(DISTINCT c."NUNOTA") AS pedidos
        FROM "TGFCAB" c
        JOIN "TGFPAR" p ON c."CODPARC" = p."CODPARC"
        WHERE c."CODVEND" = :codvend
          AND c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '2 months'
          AND c."STATUSNOTA" = 'L'
        GROUP BY p."CODPARC", p."NOMEPARC"
        ORDER BY faturamento DESC
        LIMIT 20
    ''')
    cli_result = await db.execute(cli_query, {'codvend': codvend})
    clientes = [
        {'codparc': r[0], 'nomeparc': r[1], 'faturamento': float(r[2]), 'pedidos': int(r[3])}
        for r in cli_result.fetchall()
    ]

    # Produtos do vendedor
    prod_query = text('''
        SELECT pr."CODPROD", pr."DESCRPROD",
            COALESCE(SUM(i."QTDNEG"), 0) AS qtd,
            COALESCE(SUM(i."VLRTOT"), 0) AS faturamento
        FROM "TGFCAB" c
        JOIN "TGFITE" i ON c."NUNOTA" = i."NUNOTA"
        JOIN "TGFPRO" pr ON i."CODPROD" = pr."CODPROD"
        WHERE c."CODVEND" = :codvend
          AND c."DTNEG" >= date_trunc('month', CURRENT_DATE) - INTERVAL '2 months'
          AND c."STATUSNOTA" = 'L'
        GROUP BY pr."CODPROD", pr."DESCRPROD"
        ORDER BY faturamento DESC
        LIMIT 20
    ''')
    prod_result = await db.execute(prod_query, {'codvend': codvend})
    produtos = [
        {'codprod': r[0], 'descrprod': r[1], 'qtd': float(r[2]), 'faturamento': float(r[3])}
        for r in prod_result.fetchall()
    ]

    fat_atual = float(fat[0])
    fat_anterior = float(fat[1])
    delta = round(((fat_atual - fat_anterior) / fat_anterior * 100), 2) if fat_anterior > 0 else 0

    return {
        'codvend': vend[0],
        'apelido': vend[1],
        'nomevend': vend[2],
        'fat_atual': fat_atual,
        'fat_anterior': fat_anterior,
        'delta_percentual': delta,
        'clientes': clientes,
        'produtos': produtos,
    }
