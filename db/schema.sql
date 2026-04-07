-- OpenClaw Sankhya - DDL Schema
-- Tabelas replicadas do ERP Sankhya para PostgreSQL
-- Mantendo nomes de colunas em MAIUSCULAS conforme padrao Sankhya

CREATE DATABASE openclaw_sankhya;
\c openclaw_sankhya;

-- Criar usuario da aplicacao
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'openclaw') THEN
        CREATE ROLE openclaw WITH LOGIN PASSWORD 'Oc@2026!Sx9k';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE openclaw_sankhya TO openclaw;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO openclaw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO openclaw;

-- =============================================================================
-- TGFPAR - Cadastro de Parceiros/Clientes
-- =============================================================================
CREATE TABLE IF NOT EXISTS "TGFPAR" (
    "CODPARC"       SERIAL PRIMARY KEY,
    "NOMEPARC"      VARCHAR(255) NOT NULL,
    "RAZAOSOCIAL"   VARCHAR(255),
    "TIPPESSOA"     CHAR(1) DEFAULT 'J',          -- F = Fisica, J = Juridica
    "CGCCPF"        VARCHAR(18),
    "INSCESTADUAL"  VARCHAR(20),
    "ENDERECO"      VARCHAR(255),
    "NUMEND"        VARCHAR(10),
    "COMPLEMENTO"   VARCHAR(100),
    "BAIRRO"        VARCHAR(100),
    "CIDADE"        VARCHAR(100),
    "UF"            CHAR(2),
    "CEP"           VARCHAR(10),
    "TELEFONE"      VARCHAR(20),
    "EMAIL"         VARCHAR(150),
    "ATIVO"         CHAR(1) DEFAULT 'S',
    "CLIENTE"       CHAR(1) DEFAULT 'S',
    "FORNECEDOR"    CHAR(1) DEFAULT 'N',
    "LIMCRED"       NUMERIC(15,2) DEFAULT 0,
    "CODCID"        INTEGER,
    "DTALTER"       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "DTCAD"         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tgfpar_nomeparc ON "TGFPAR" ("NOMEPARC");
CREATE INDEX idx_tgfpar_cidade ON "TGFPAR" ("CIDADE");
CREATE INDEX idx_tgfpar_uf ON "TGFPAR" ("UF");
CREATE INDEX idx_tgfpar_cgccpf ON "TGFPAR" ("CGCCPF");

-- =============================================================================
-- TGFVEND - Cadastro de Vendedores
-- =============================================================================
CREATE TABLE IF NOT EXISTS "TGFVEND" (
    "CODVEND"       SERIAL PRIMARY KEY,
    "APELIDO"       VARCHAR(50) NOT NULL,
    "NOMEVEND"      VARCHAR(255) NOT NULL,
    "CODGER"        INTEGER,                       -- Codigo do gerente
    "ATIVO"         CHAR(1) DEFAULT 'S',
    "COMISSAO"      NUMERIC(5,2) DEFAULT 0,
    "TELEFONE"      VARCHAR(20),
    "EMAIL"         VARCHAR(150),
    "CODPARC"       INTEGER,                       -- Parceiro vinculado
    "DTALTER"       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "DTCAD"         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tgfvend_apelido ON "TGFVEND" ("APELIDO");
CREATE INDEX idx_tgfvend_ativo ON "TGFVEND" ("ATIVO");

-- =============================================================================
-- TGFPRO - Cadastro de Produtos
-- =============================================================================
CREATE TABLE IF NOT EXISTS "TGFPRO" (
    "CODPROD"       SERIAL PRIMARY KEY,
    "DESCRPROD"     VARCHAR(255) NOT NULL,
    "REFERENCIA"    VARCHAR(50),
    "CODGRUPOPROD"  INTEGER,
    "MARCA"         VARCHAR(100),
    "UNIDADE"       VARCHAR(5) DEFAULT 'UN',
    "ATIVO"         CHAR(1) DEFAULT 'S',
    "VLRCUSTO"      NUMERIC(15,2) DEFAULT 0,
    "VLRVENDA"      NUMERIC(15,2) DEFAULT 0,
    "ESTOQUE"       NUMERIC(15,2) DEFAULT 0,
    "ESTMIN"        NUMERIC(15,2) DEFAULT 0,
    "PESOBRUTO"     NUMERIC(10,3) DEFAULT 0,
    "NCM"           VARCHAR(10),
    "CODBARRAS"     VARCHAR(20),
    "DTALTER"       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "DTCAD"         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tgfpro_descrprod ON "TGFPRO" ("DESCRPROD");
CREATE INDEX idx_tgfpro_codgrupoprod ON "TGFPRO" ("CODGRUPOPROD");
CREATE INDEX idx_tgfpro_marca ON "TGFPRO" ("MARCA");
CREATE INDEX idx_tgfpro_referencia ON "TGFPRO" ("REFERENCIA");

-- =============================================================================
-- TGFCAB - Cabecalho de Notas/Pedidos
-- =============================================================================
CREATE TABLE IF NOT EXISTS "TGFCAB" (
    "NUNOTA"        SERIAL PRIMARY KEY,
    "NUMNOTA"       INTEGER,
    "CODPARC"       INTEGER NOT NULL REFERENCES "TGFPAR"("CODPARC"),
    "CODVEND"       INTEGER NOT NULL REFERENCES "TGFVEND"("CODVEND"),
    "CODTIPOPER"    INTEGER DEFAULT 0,             -- Tipo de operacao (venda, devolucao, etc)
    "DTNEG"         TIMESTAMP NOT NULL,            -- Data de negociacao
    "DTFATUR"       TIMESTAMP,                     -- Data de faturamento
    "VLRNOTA"       NUMERIC(15,2) NOT NULL DEFAULT 0,
    "VLRDESC"       NUMERIC(15,2) DEFAULT 0,
    "VLRFRETE"      NUMERIC(15,2) DEFAULT 0,
    "VLRICMSSUB"    NUMERIC(15,2) DEFAULT 0,
    "CODCENCUS"     INTEGER,                       -- Centro de custo
    "CODNAT"        INTEGER,                       -- Natureza
    "CODEMP"        INTEGER DEFAULT 1,             -- Empresa
    "CODTIPVENDA"   INTEGER DEFAULT 0,
    "STATUSNOTA"    CHAR(1) DEFAULT 'L',           -- L=Liberada, P=Pendente, C=Cancelada
    "OBSERVACAO"    TEXT,
    "DTALTER"       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tgfcab_codparc ON "TGFCAB" ("CODPARC");
CREATE INDEX idx_tgfcab_codvend ON "TGFCAB" ("CODVEND");
CREATE INDEX idx_tgfcab_dtneg ON "TGFCAB" ("DTNEG");
CREATE INDEX idx_tgfcab_statusnota ON "TGFCAB" ("STATUSNOTA");
CREATE INDEX idx_tgfcab_numnota ON "TGFCAB" ("NUMNOTA");

-- =============================================================================
-- TGFITE - Itens das Notas/Pedidos
-- =============================================================================
CREATE TABLE IF NOT EXISTS "TGFITE" (
    "NUNOTA"        INTEGER NOT NULL REFERENCES "TGFCAB"("NUNOTA") ON DELETE CASCADE,
    "SEQUENCIA"     INTEGER NOT NULL,
    "CODPROD"       INTEGER NOT NULL REFERENCES "TGFPRO"("CODPROD"),
    "QTDNEG"        NUMERIC(15,2) NOT NULL DEFAULT 0,
    "VLRUNIT"       NUMERIC(15,2) NOT NULL DEFAULT 0,
    "VLRTOT"        NUMERIC(15,2) NOT NULL DEFAULT 0,
    "VLRDESC"       NUMERIC(15,2) DEFAULT 0,
    "CODVOL"        VARCHAR(5) DEFAULT 'UN',       -- Unidade de volume
    "VLRICMS"       NUMERIC(15,2) DEFAULT 0,
    "VLRIPI"        NUMERIC(15,2) DEFAULT 0,
    "CODCFO"        INTEGER,                       -- CFOP
    "ATUALESTOQUE"  CHAR(1) DEFAULT 'S',
    PRIMARY KEY ("NUNOTA", "SEQUENCIA")
);

CREATE INDEX idx_tgfite_codprod ON "TGFITE" ("CODPROD");
CREATE INDEX idx_tgfite_nunota ON "TGFITE" ("NUNOTA");

-- Garantir permissoes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO openclaw;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO openclaw;
