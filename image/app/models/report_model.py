from core.configs import settings
from sqlalchemy import Column, Integer, String, Text, DateTime, CHAR
from sqlalchemy.sql import func


class AgentReport(settings.DBBaseModel):
    '''Historico de relatorios gerados pelo agente.'''
    __tablename__ = 'agent_reports'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    agent_name = Column(String(100), nullable=False)
    report_text = Column(Text, nullable=False)
    score = Column(Integer)
    status = Column(String(20), default='generated')  # generated, sent, failed
    whatsapp_sent = Column(CHAR(1), default='N')
    created_at = Column(DateTime, default=func.now())

    def __str__(self):
        return f'<AgentReport: {self.id} - {self.agent_name}>'
