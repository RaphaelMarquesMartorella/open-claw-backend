from typing import ClassVar
from urllib.parse import quote
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    '''Configuracoes gerais da aplicacao OpenClaw.'''

    API_V1_STR: str = '/api/v1'
    API_VERSION: str = '1.0.0'
    DB_SCHEMA: str = 'public'
    DBBaseModel: ClassVar = declarative_base()

    # Banco de dados PostgreSQL
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_NAME: str = os.getenv('DB_NAME', 'openclaw_sankhya')
    DB_USER: str = os.getenv('DB_USER', 'openclaw')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')

    # WhatsApp
    WHATSAPP_API_URL: str = os.getenv('WHATSAPP_API_URL', '')
    WHATSAPP_API_KEY: str = os.getenv('WHATSAPP_API_KEY', '')
    WHATSAPP_DIRECTOR_NUMBER: str = os.getenv('WHATSAPP_DIRECTOR_NUMBER', '')

    # Agente
    AGENT_SCHEDULE: str = os.getenv('AGENT_SCHEDULE', '08:00')
    AGENT_TIMEZONE: str = os.getenv('AGENT_TIMEZONE', 'America/Recife')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    # CORS
    CORS_ORIGINS: list = [
        'http://localhost:3000',
        'http://129.121.54.176',
        'http://129.121.54.176:3000',
    ]

    @property
    def DB_URL(self) -> str:
        '''Gera a URL do banco de dados async.'''
        encoded_password = quote(self.DB_PASSWORD)
        return f'postgresql+asyncpg://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DB_URL_SYNC(self) -> str:
        '''Gera a URL do banco de dados sync.'''
        encoded_password = quote(self.DB_PASSWORD)
        return f'postgresql+psycopg2://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'allow'


settings: Settings = Settings()
