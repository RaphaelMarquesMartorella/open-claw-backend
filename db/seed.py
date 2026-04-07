#!/usr/bin/env python3
'''
Seed de dados ficticios realistas para as tabelas Sankhya no PostgreSQL.
Gera dados para os ultimos 3 meses com variacao intencional de performance.
Contexto: Pneubras - distribuidora de pneus e afins.
'''
import os
import random
import psycopg2
from datetime import datetime, timedelta
from decimal import Decimal

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'openclaw_sankhya')
DB_USER = os.environ.get('DB_USER', 'openclaw')
DB_PASS = os.environ.get('DB_PASS', 'Oc@2026!Sx9k')


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def seed_vendedores(cur):
    '''Insere 10 vendedores.'''
    vendedores = [
        ('Carlos', 'Carlos Eduardo Silva', 3.5, '81999110001', 'carlos.silva@pneubras.com.br'),
        ('Marcos', 'Marcos Aurelio Santos', 3.0, '81999110002', 'marcos.santos@pneubras.com.br'),
        ('Fernanda', 'Fernanda Oliveira Costa', 4.0, '81999110003', 'fernanda.costa@pneubras.com.br'),
        ('Roberto', 'Roberto Almeida Junior', 3.5, '81999110004', 'roberto.junior@pneubras.com.br'),
        ('Patricia', 'Patricia Souza Lima', 3.0, '81999110005', 'patricia.lima@pneubras.com.br'),
        ('Anderson', 'Anderson Pereira Gomes', 3.5, '81999110006', 'anderson.gomes@pneubras.com.br'),
        ('Juliana', 'Juliana Barbosa Reis', 4.0, '81999110007', 'juliana.reis@pneubras.com.br'),
        ('Ricardo', 'Ricardo Mendes Filho', 3.0, '81999110008', 'ricardo.mendes@pneubras.com.br'),
        ('Camila', 'Camila Ferreira Nunes', 3.5, '81999110009', 'camila.nunes@pneubras.com.br'),
        ('Diego', 'Diego Rocha Cavalcanti', 3.0, '81999110010', 'diego.rocha@pneubras.com.br'),
    ]
    for apelido, nome, comissao, tel, email in vendedores:
        cur.execute('''
            INSERT INTO "TGFVEND" ("APELIDO", "NOMEVEND", "COMISSAO", "TELEFONE", "EMAIL", "ATIVO")
            VALUES (%s, %s, %s, %s, %s, 'S')
        ''', (apelido, nome, comissao, tel, email))
    print(f'  -> {len(vendedores)} vendedores inseridos')


def seed_parceiros(cur):
    '''Insere 50 clientes com cidades variadas do Nordeste.'''
    cidades_ne = [
        ('Recife', 'PE'), ('Fortaleza', 'CE'), ('Salvador', 'BA'),
        ('Natal', 'RN'), ('Joao Pessoa', 'PB'), ('Maceio', 'AL'),
        ('Aracaju', 'SE'), ('Teresina', 'PI'), ('Sao Luis', 'MA'),
        ('Caruaru', 'PE'), ('Petrolina', 'PE'), ('Campina Grande', 'PB'),
        ('Feira de Santana', 'BA'), ('Garanhuns', 'PE'), ('Juazeiro do Norte', 'CE'),
        ('Mossoró', 'RN'), ('Parnamirim', 'RN'), ('Olinda', 'PE'),
        ('Jaboatao', 'PE'), ('Paulista', 'PE'),
    ]

    nomes_empresas = [
        'Auto Center', 'Pneus & Rodas', 'Borracharia', 'Mecanica',
        'Auto Pecas', 'Centro Automotivo', 'Garage', 'Auto Service',
        'Rodas & Pneus', 'Pneumaticos',
    ]

    sobrenomes = [
        'Silva', 'Santos', 'Oliveira', 'Souza', 'Lima', 'Pereira',
        'Costa', 'Ferreira', 'Almeida', 'Barbosa', 'Rocha', 'Cavalcanti',
        'Gomes', 'Martins', 'Araujo', 'Melo', 'Ribeiro', 'Cardoso',
    ]

    for i in range(1, 51):
        cidade, uf = random.choice(cidades_ne)
        nome_tipo = random.choice(nomes_empresas)
        sobrenome = random.choice(sobrenomes)
        nome = f'{nome_tipo} {sobrenome}'
        razao = f'{nome} LTDA'
        cnpj = f'{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/0001-{random.randint(10,99)}'
        telefone = f'({random.randint(71,99)}){random.randint(90000,99999)}-{random.randint(1000,9999)}'
        email = f'contato{i}@{sobrenome.lower()}auto.com.br'
        lim_cred = random.choice([10000, 25000, 50000, 75000, 100000, 150000, 200000])
        bairro = random.choice(['Centro', 'Boa Viagem', 'Boa Vista', 'Madalena', 'Imbiribeira', 'Afogados', 'Derby', 'Pina'])

        cur.execute('''
            INSERT INTO "TGFPAR" ("NOMEPARC", "RAZAOSOCIAL", "TIPPESSOA", "CGCCPF",
                "CIDADE", "UF", "TELEFONE", "EMAIL", "LIMCRED", "BAIRRO", "ENDERECO", "CEP")
            VALUES (%s, %s, 'J', %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nome, razao, cnpj, cidade, uf, telefone, email, lim_cred, bairro,
              f'Rua {sobrenome}, {random.randint(1,999)}', f'{random.randint(50000,60000)}-{random.randint(100,999)}'))

    print('  -> 50 parceiros inseridos')


def seed_produtos(cur):
    '''Insere 100 produtos (pneus e afins).'''
    marcas = ['Pirelli', 'Michelin', 'Goodyear', 'Continental', 'Bridgestone',
              'Firestone', 'Dunlop', 'Yokohama', 'Hankook', 'Kumho']

    tipos_pneu = [
        ('Pneu', 175, 70, 13), ('Pneu', 185, 65, 14), ('Pneu', 195, 55, 15),
        ('Pneu', 205, 55, 16), ('Pneu', 215, 50, 17), ('Pneu', 225, 45, 17),
        ('Pneu', 225, 50, 18), ('Pneu', 235, 55, 18), ('Pneu', 245, 45, 19),
        ('Pneu', 255, 40, 19), ('Pneu', 265, 65, 17), ('Pneu', 275, 70, 16),
        ('Pneu', 175, 65, 14), ('Pneu', 185, 70, 14), ('Pneu', 195, 65, 15),
        ('Pneu', 205, 60, 15), ('Pneu', 205, 65, 16), ('Pneu', 215, 55, 17),
        ('Pneu', 225, 55, 17), ('Pneu', 235, 60, 18),
    ]

    acessorios = [
        ('Camara de Ar Aro 13', 'Acessorios', 25, 45, 200),
        ('Camara de Ar Aro 14', 'Acessorios', 28, 50, 180),
        ('Camara de Ar Aro 15', 'Acessorios', 30, 55, 160),
        ('Camara de Ar Aro 16', 'Acessorios', 35, 60, 140),
        ('Protetor de Aro 13', 'Acessorios', 12, 22, 300),
        ('Protetor de Aro 14', 'Acessorios', 14, 25, 280),
        ('Protetor de Aro 15', 'Acessorios', 15, 28, 260),
        ('Bico de Pneu Cromado (jg)', 'Acessorios', 8, 18, 500),
        ('Bico de Pneu Preto (jg)', 'Acessorios', 5, 12, 600),
        ('Calibrador Manual', 'Ferramentas', 45, 85, 50),
        ('Chave de Roda Cruz', 'Ferramentas', 35, 65, 80),
        ('Macaco Hidraulico 2T', 'Ferramentas', 120, 220, 40),
        ('Cera para Pneu 500ml', 'Quimicos', 18, 35, 300),
        ('Limpa Pneu Spray', 'Quimicos', 15, 28, 350),
        ('Selante para Pneu', 'Quimicos', 22, 42, 200),
        ('Roda de Ferro Aro 13', 'Rodas', 80, 150, 100),
        ('Roda de Ferro Aro 14', 'Rodas', 90, 170, 90),
        ('Roda de Ferro Aro 15', 'Rodas', 100, 190, 80),
        ('Roda de Liga Leve Aro 15', 'Rodas', 250, 480, 60),
        ('Roda de Liga Leve Aro 17', 'Rodas', 350, 650, 40),
    ]

    prod_count = 0

    # Pneus (80 produtos)
    for marca in marcas:
        tipos_selecionados = random.sample(tipos_pneu, 8)
        for tipo, larg, perf, aro in tipos_selecionados:
            descr = f'{tipo} {marca} {larg}/{perf}R{aro}'
            ref = f'{marca[:3].upper()}{larg}{perf}R{aro}'
            custo = round(random.uniform(180, 600), 2)
            venda = round(custo * random.uniform(1.25, 1.60), 2)
            estoque = random.randint(5, 120)
            estmin = random.randint(5, 20)
            peso = round(random.uniform(6, 14), 3)
            ncm = '40111000'
            grupo = 1  # Pneus

            cur.execute('''
                INSERT INTO "TGFPRO" ("DESCRPROD", "REFERENCIA", "CODGRUPOPROD", "MARCA",
                    "VLRCUSTO", "VLRVENDA", "ESTOQUE", "ESTMIN", "PESOBRUTO", "NCM", "ATIVO")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'S')
            ''', (descr, ref, grupo, marca, custo, venda, estoque, estmin, peso, ncm))
            prod_count += 1

    # Acessorios (20 produtos)
    for descr, grupo_nome, custo, venda, estoque in acessorios:
        grupo = 2 if grupo_nome == 'Acessorios' else 3 if grupo_nome == 'Ferramentas' else 4 if grupo_nome == 'Quimicos' else 5
        cur.execute('''
            INSERT INTO "TGFPRO" ("DESCRPROD", "REFERENCIA", "CODGRUPOPROD", "MARCA",
                "VLRCUSTO", "VLRVENDA", "ESTOQUE", "ESTMIN", "PESOBRUTO", "NCM", "ATIVO")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'S')
        ''', (descr, descr[:10].upper().replace(' ', ''), grupo, 'Nacional',
              custo, venda, estoque, 10, round(random.uniform(0.5, 5), 3), '40000000'))
        prod_count += 1

    print(f'  -> {prod_count} produtos inseridos')


def seed_pedidos(cur):
    '''
    Gera ~500 pedidos nos ultimos 3 meses.
    Mes atual (abril/2026) com performance ~15% abaixo do mes anterior para 3+ vendedores.
    '''
    hoje = datetime(2026, 4, 7)

    # Definir periodos
    mes_atual_inicio = datetime(2026, 4, 1)
    mes_anterior_inicio = datetime(2026, 3, 1)
    mes_retrasado_inicio = datetime(2026, 2, 1)

    # Buscar IDs
    cur.execute('SELECT "CODPARC" FROM "TGFPAR"')
    parceiros = [r[0] for r in cur.fetchall()]

    cur.execute('SELECT "CODVEND" FROM "TGFVEND"')
    vendedores = [r[0] for r in cur.fetchall()]

    cur.execute('SELECT "CODPROD", "VLRVENDA" FROM "TGFPRO"')
    produtos = [(r[0], float(r[1])) for r in cur.fetchall()]

    # Vendedores que terao queda no mes atual (indices 0,1,2 = Carlos, Marcos, Fernanda)
    vendedores_queda = set(vendedores[:3])
    # Vendedores que terao queda moderada (indices 3,4 = Roberto, Patricia)
    vendedores_queda_leve = set(vendedores[3:5])

    # Clientes que vao "sumir" no mes atual (10 clientes)
    clientes_inativos_mes_atual = set(random.sample(parceiros, 10))

    total_notas = 0
    total_itens = 0
    numnota = 1000

    def gerar_pedidos_periodo(dt_inicio, dt_fim, qtd_pedidos, fator_vendedor=None):
        nonlocal total_notas, total_itens, numnota

        for _ in range(qtd_pedidos):
            # Escolher vendedor
            vendedor = random.choice(vendedores)

            # Aplicar fator de reducao se necessario
            if fator_vendedor and vendedor in fator_vendedor:
                if random.random() > fator_vendedor[vendedor]:
                    continue  # Pula este pedido (simula queda)

            # Escolher parceiro
            if dt_inicio.month == 4 and dt_inicio.year == 2026:
                # No mes atual, clientes inativos nao compram
                parceiro_pool = [p for p in parceiros if p not in clientes_inativos_mes_atual]
            else:
                parceiro_pool = parceiros

            parceiro = random.choice(parceiro_pool)

            # Data aleatoria no periodo
            dias_range = (dt_fim - dt_inicio).days
            if dias_range <= 0:
                dias_range = 1
            dt_neg = dt_inicio + timedelta(days=random.randint(0, dias_range - 1),
                                           hours=random.randint(8, 17),
                                           minutes=random.randint(0, 59))

            numnota += 1

            # Gerar itens (2 a 5 por nota)
            qtd_itens = random.randint(2, 5)
            produtos_nota = random.sample(produtos, min(qtd_itens, len(produtos)))

            vlr_total_nota = 0
            itens_data = []

            for seq, (codprod, vlr_venda) in enumerate(produtos_nota, 1):
                qtd = random.randint(1, 20)
                # Variacao de preco (desconto ou preco cheio)
                vlr_unit = round(vlr_venda * random.uniform(0.85, 1.0), 2)
                vlr_tot = round(qtd * vlr_unit, 2)
                vlr_desc = round(random.uniform(0, vlr_tot * 0.05), 2)
                vlr_tot_final = round(vlr_tot - vlr_desc, 2)

                itens_data.append((seq, codprod, qtd, vlr_unit, vlr_tot_final, vlr_desc))
                vlr_total_nota += vlr_tot_final

            vlr_total_nota = round(vlr_total_nota, 2)

            # Inserir cabecalho
            cur.execute('''
                INSERT INTO "TGFCAB" ("NUMNOTA", "CODPARC", "CODVEND", "CODTIPOPER", "DTNEG",
                    "DTFATUR", "VLRNOTA", "VLRDESC", "STATUSNOTA", "CODEMP")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "NUNOTA"
            ''', (numnota, parceiro, vendedor, random.choice([1001, 1002, 1003]),
                  dt_neg, dt_neg + timedelta(days=random.randint(0, 2)),
                  vlr_total_nota, round(random.uniform(0, vlr_total_nota * 0.03), 2),
                  random.choices(['L', 'P'], weights=[90, 10])[0], 1))

            nunota = cur.fetchone()[0]
            total_notas += 1

            # Inserir itens
            for seq, codprod, qtd, vlr_unit, vlr_tot, vlr_desc in itens_data:
                cur.execute('''
                    INSERT INTO "TGFITE" ("NUNOTA", "SEQUENCIA", "CODPROD", "QTDNEG",
                        "VLRUNIT", "VLRTOT", "VLRDESC")
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (nunota, seq, codprod, qtd, vlr_unit, vlr_tot, vlr_desc))
                total_itens += 1

    # Mes retrasado (fevereiro): ~160 pedidos - baseline
    gerar_pedidos_periodo(
        mes_retrasado_inicio,
        datetime(2026, 2, 28),
        160
    )

    # Mes anterior (marco): ~200 pedidos - pico (melhor mes)
    gerar_pedidos_periodo(
        mes_anterior_inicio,
        datetime(2026, 3, 31),
        200
    )

    # Mes atual (abril 1-7): ~80 pedidos proporcionais, com queda para vendedores especificos
    # Para 7 dias de abril, ~80 pedidos e normal
    # Vendedores em queda: geram ~15-25% menos pedidos
    fator_queda = {}
    for v in vendedores_queda:
        fator_queda[v] = 0.65  # 35% dos pedidos cortados = queda significativa
    for v in vendedores_queda_leve:
        fator_queda[v] = 0.80  # 20% dos pedidos cortados

    gerar_pedidos_periodo(
        mes_atual_inicio,
        hoje,
        100,  # Gerar mais tentativas para compensar os cortados
        fator_vendedor=fator_queda
    )

    print(f'  -> {total_notas} notas/pedidos inseridos')
    print(f'  -> {total_itens} itens inseridos')
    return clientes_inativos_mes_atual


def verify_counts(cur):
    '''Verifica contagem de registros.'''
    tables = ['TGFPAR', 'TGFVEND', 'TGFPRO', 'TGFCAB', 'TGFITE']
    print('\n=== Contagem de registros ===')
    for t in tables:
        cur.execute(f'SELECT COUNT(*) FROM "{t}"')
        count = cur.fetchone()[0]
        print(f'  {t}: {count} registros')


def main():
    print('=== Seed OpenClaw Sankhya ===\n')

    conn = get_conn()
    conn.autocommit = False
    cur = conn.cursor()

    try:
        # Limpar tabelas (ordem por FK)
        print('Limpando tabelas...')
        cur.execute('DELETE FROM "TGFITE"')
        cur.execute('DELETE FROM "TGFCAB"')
        cur.execute('DELETE FROM "TGFPRO"')
        cur.execute('DELETE FROM "TGFVEND"')
        cur.execute('DELETE FROM "TGFPAR"')

        # Resetar sequences
        cur.execute('ALTER SEQUENCE "TGFPAR_CODPARC_seq" RESTART WITH 1')
        cur.execute('ALTER SEQUENCE "TGFVEND_CODVEND_seq" RESTART WITH 1')
        cur.execute('ALTER SEQUENCE "TGFPRO_CODPROD_seq" RESTART WITH 1')
        cur.execute('ALTER SEQUENCE "TGFCAB_NUNOTA_seq" RESTART WITH 1')

        random.seed(42)  # Reprodutibilidade

        print('\nInserindo vendedores...')
        seed_vendedores(cur)

        print('\nInserindo parceiros...')
        seed_parceiros(cur)

        print('\nInserindo produtos...')
        seed_produtos(cur)

        print('\nInserindo pedidos e itens...')
        inativos = seed_pedidos(cur)

        conn.commit()
        print('\n--- Commit OK ---')

        verify_counts(cur)

        # Mostrar resumo de vendedores inativos
        print(f'\nClientes inativos no mes atual (CODPARC): {sorted(inativos)}')

    except Exception as e:
        conn.rollback()
        print(f'\nERRO: {e}')
        raise
    finally:
        cur.close()
        conn.close()

    print('\n=== Seed concluido com sucesso! ===')


if __name__ == '__main__':
    main()
