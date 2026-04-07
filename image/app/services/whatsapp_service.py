'''Service de envio de mensagens via WhatsApp.'''
import logging
import json
from core.configs import settings
from core.httpx_client import http_client

logger = logging.getLogger('AGENT.WHATSAPP')


async def send_whatsapp_report_service(report_text: str) -> dict:
    '''Envia relatorio via WhatsApp. Retorna status do envio.'''

    number = settings.WHATSAPP_DIRECTOR_NUMBER
    api_url = settings.WHATSAPP_API_URL
    api_key = settings.WHATSAPP_API_KEY

    if not api_url or not api_key or not number:
        logger.warning('WhatsApp nao configurado. Logando payload...')
        payload = {
            'number': number or 'NAO_CONFIGURADO',
            'text': report_text,
        }
        logger.info(f'WHATSAPP PAYLOAD (mock): {json.dumps(payload, ensure_ascii=False)[:500]}...')
        return {
            'status': 'mock',
            'message': 'WhatsApp nao configurado. Payload logado.',
            'payload': payload,
        }

    try:
        # Formato compativel com Evolution API / Z-API / Meta Cloud API
        payload = {
            'number': number,
            'text': report_text,
        }

        headers = {
            'Content-Type': 'application/json',
            'apikey': api_key,
        }

        # Tenta Evolution API format
        url = f'{api_url}/message/sendText/openclaw'

        response = await http_client.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        logger.info(f'WhatsApp enviado com sucesso para {number}')
        return {
            'status': 'sent',
            'message': f'Relatorio enviado para {number}',
            'response': response.json(),
        }

    except Exception as ex:
        logger.error(f'Erro ao enviar WhatsApp: {ex}')
        return {
            'status': 'error',
            'message': str(ex),
        }
