from pydantic import BaseModel
from datetime import datetime


class KPIResponse(BaseModel):
    '''KPIs do dashboard.'''
    faturamento_atual: float
    faturamento_anterior: float
    delta_percentual: float
    clientes_ativos: int
    total_pedidos_atual: int
    total_pedidos_anterior: int
    ticket_medio_atual: float
    ticket_medio_anterior: float

    class Config:
        from_attributes = True


class VendedorRankingItem(BaseModel):
    '''Item do ranking de vendedores.'''
    codvend: int
    apelido: str
    nomevend: str
    fat_atual: float
    fat_anterior: float
    delta_percentual: float
    qtd_pedidos_atual: int
    qtd_pedidos_anterior: int

    class Config:
        from_attributes = True


class VendedorRankingResponse(BaseModel):
    '''Resposta do ranking de vendedores.'''
    vendedores: list[VendedorRankingItem]

    class Config:
        from_attributes = True


class VendedorDetalheResponse(BaseModel):
    '''Detalhe de vendedor com breakdown.'''
    codvend: int
    apelido: str
    nomevend: str
    fat_atual: float
    fat_anterior: float
    delta_percentual: float
    clientes: list[dict]
    produtos: list[dict]

    class Config:
        from_attributes = True


class ProdutoRankingItem(BaseModel):
    '''Item do ranking de produtos.'''
    codprod: int
    descrprod: str
    marca: str | None
    qtd_vendida: float
    faturamento: float
    estoque: float
    giro: float

    class Config:
        from_attributes = True


class ProdutoRankingResponse(BaseModel):
    '''Resposta do ranking de produtos.'''
    produtos: list[ProdutoRankingItem]

    class Config:
        from_attributes = True


class ClienteInativoItem(BaseModel):
    '''Item de cliente inativo.'''
    codparc: int
    nomeparc: str
    cidade: str | None
    uf: str | None
    valor_anterior: float
    ultimo_pedido: str | None
    vendedor_responsavel: str | None

    class Config:
        from_attributes = True


class ClienteInativoResponse(BaseModel):
    '''Resposta de clientes inativos.'''
    clientes: list[ClienteInativoItem]
    valor_total_risco: float

    class Config:
        from_attributes = True


class ComparativoDiarioItem(BaseModel):
    '''Faturamento diario.'''
    data: str
    faturamento: float

    class Config:
        from_attributes = True


class ComparativoDiarioResponse(BaseModel):
    '''Resposta do comparativo diario.'''
    dias: list[ComparativoDiarioItem]

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    '''Resposta de relatorio do agente.'''
    id: int
    agent_name: str
    report_text: str
    score: int | None
    status: str
    whatsapp_sent: str
    created_at: datetime | None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%d/%m/%Y %H:%M') if v else None
        }


class ReportListResponse(BaseModel):
    '''Lista de relatorios.'''
    reports: list[ReportResponse]

    class Config:
        from_attributes = True


class AgentTriggerResponse(BaseModel):
    '''Resposta do disparo do agente.'''
    status: str
    message: str
    report_id: int | None = None

    class Config:
        from_attributes = True
