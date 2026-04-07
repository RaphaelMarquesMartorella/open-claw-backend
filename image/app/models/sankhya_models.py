from core.configs import settings
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, CHAR
from sqlalchemy.sql import func


class TGFPAR(settings.DBBaseModel):
    '''Cadastro de Parceiros/Clientes.'''
    __tablename__ = 'TGFPAR'

    CODPARC = Column(Integer, primary_key=True, autoincrement=True, index=True)
    NOMEPARC = Column(String(255), nullable=False)
    RAZAOSOCIAL = Column(String(255))
    TIPPESSOA = Column(CHAR(1), default='J')
    CGCCPF = Column(String(18))
    INSCESTADUAL = Column(String(20))
    ENDERECO = Column(String(255))
    NUMEND = Column(String(10))
    COMPLEMENTO = Column(String(100))
    BAIRRO = Column(String(100))
    CIDADE = Column(String(100))
    UF = Column(CHAR(2))
    CEP = Column(String(10))
    TELEFONE = Column(String(20))
    EMAIL = Column(String(150))
    ATIVO = Column(CHAR(1), default='S')
    CLIENTE = Column(CHAR(1), default='S')
    FORNECEDOR = Column(CHAR(1), default='N')
    LIMCRED = Column(Numeric(15, 2), default=0)
    CODCID = Column(Integer)
    DTALTER = Column(DateTime, default=func.now())
    DTCAD = Column(DateTime, default=func.now())

    def __str__(self):
        return f'<TGFPAR: {self.CODPARC} - {self.NOMEPARC}>'


class TGFVEND(settings.DBBaseModel):
    '''Cadastro de Vendedores.'''
    __tablename__ = 'TGFVEND'

    CODVEND = Column(Integer, primary_key=True, autoincrement=True, index=True)
    APELIDO = Column(String(50), nullable=False)
    NOMEVEND = Column(String(255), nullable=False)
    CODGER = Column(Integer)
    ATIVO = Column(CHAR(1), default='S')
    COMISSAO = Column(Numeric(5, 2), default=0)
    TELEFONE = Column(String(20))
    EMAIL = Column(String(150))
    CODPARC = Column(Integer)
    DTALTER = Column(DateTime, default=func.now())
    DTCAD = Column(DateTime, default=func.now())

    def __str__(self):
        return f'<TGFVEND: {self.CODVEND} - {self.APELIDO}>'


class TGFPRO(settings.DBBaseModel):
    '''Cadastro de Produtos.'''
    __tablename__ = 'TGFPRO'

    CODPROD = Column(Integer, primary_key=True, autoincrement=True, index=True)
    DESCRPROD = Column(String(255), nullable=False)
    REFERENCIA = Column(String(50))
    CODGRUPOPROD = Column(Integer)
    MARCA = Column(String(100))
    UNIDADE = Column(String(5), default='UN')
    ATIVO = Column(CHAR(1), default='S')
    VLRCUSTO = Column(Numeric(15, 2), default=0)
    VLRVENDA = Column(Numeric(15, 2), default=0)
    ESTOQUE = Column(Numeric(15, 2), default=0)
    ESTMIN = Column(Numeric(15, 2), default=0)
    PESOBRUTO = Column(Numeric(10, 3), default=0)
    NCM = Column(String(10))
    CODBARRAS = Column(String(20))
    DTALTER = Column(DateTime, default=func.now())
    DTCAD = Column(DateTime, default=func.now())

    def __str__(self):
        return f'<TGFPRO: {self.CODPROD} - {self.DESCRPROD}>'


class TGFCAB(settings.DBBaseModel):
    '''Cabecalho de Notas/Pedidos.'''
    __tablename__ = 'TGFCAB'

    NUNOTA = Column(Integer, primary_key=True, autoincrement=True, index=True)
    NUMNOTA = Column(Integer)
    CODPARC = Column(Integer, nullable=False)
    CODVEND = Column(Integer, nullable=False)
    CODTIPOPER = Column(Integer, default=0)
    DTNEG = Column(DateTime, nullable=False)
    DTFATUR = Column(DateTime)
    VLRNOTA = Column(Numeric(15, 2), nullable=False, default=0)
    VLRDESC = Column(Numeric(15, 2), default=0)
    VLRFRETE = Column(Numeric(15, 2), default=0)
    VLRICMSSUB = Column(Numeric(15, 2), default=0)
    CODCENCUS = Column(Integer)
    CODNAT = Column(Integer)
    CODEMP = Column(Integer, default=1)
    CODTIPVENDA = Column(Integer, default=0)
    STATUSNOTA = Column(CHAR(1), default='L')
    OBSERVACAO = Column(Text)
    DTALTER = Column(DateTime, default=func.now())

    def __str__(self):
        return f'<TGFCAB: {self.NUNOTA} - R${self.VLRNOTA}>'


class TGFITE(settings.DBBaseModel):
    '''Itens das Notas/Pedidos.'''
    __tablename__ = 'TGFITE'

    NUNOTA = Column(Integer, primary_key=True)
    SEQUENCIA = Column(Integer, primary_key=True)
    CODPROD = Column(Integer, nullable=False)
    QTDNEG = Column(Numeric(15, 2), nullable=False, default=0)
    VLRUNIT = Column(Numeric(15, 2), nullable=False, default=0)
    VLRTOT = Column(Numeric(15, 2), nullable=False, default=0)
    VLRDESC = Column(Numeric(15, 2), default=0)
    CODVOL = Column(String(5), default='UN')
    VLRICMS = Column(Numeric(15, 2), default=0)
    VLRIPI = Column(Numeric(15, 2), default=0)
    CODCFO = Column(Integer)
    ATUALESTOQUE = Column(CHAR(1), default='S')

    def __str__(self):
        return f'<TGFITE: {self.NUNOTA}/{self.SEQUENCIA}>'
