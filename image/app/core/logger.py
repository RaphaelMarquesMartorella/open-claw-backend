import logging
import warnings
import sys


def setup_logging():
    '''Configura o logging da aplicacao.'''
    warnings.filterwarnings('ignore', message='.*SQLAlchemy.*')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('apscheduler').setLevel(logging.WARNING)


logger_agent = logging.getLogger('AGENT.GESTOR_COMERCIAL')
logger_whatsapp = logging.getLogger('AGENT.WHATSAPP')
