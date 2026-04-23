'''Service de envio de mensagens via WhatsApp (microservico wweb.js).'''
import logging
import json
import httpx
from core.configs import settings

logger = logging.getLogger('AGENT.WHATSAPP')


async def send_whatsapp_report_service(report_text: str) -> dict:
    '''Envia relatorio via WhatsApp chamando o microservico Node (whatsapp-web.js).'''

    number = settings.WHATSAPP_DIRECTOR_NUMBER
    api_url = settings.WHATSAPP_API_URL

    if not api_url or not number:
        logger.warning('WhatsApp nao configurado. Logando payload...')
        payload = {'number': number or 'NAO_CONFIGURADO', 'text': report_text}
        logger.info(f'WHATSAPP PAYLOAD (mock): {json.dumps(payload, ensure_ascii=False)[:500]}...')
        return {
            'status': 'mock',
            'message': 'WhatsApp nao configurado. Payload logado.',
            'payload': payload,
        }

    url = f'{api_url.rstrip("/")}/send-message'
    payload = {'number': number, 'text': report_text}

    try:
        async with httpx.AsyncClient(timeout=60) as http:
            response = await http.post(url, json=payload)
            data = response.json() if response.content else {}

        if response.status_code >= 400:
            logger.error(f'wweb.js respondeu {response.status_code}: {data}')
            return {'status': 'error', 'message': data.get('message', f'HTTP {response.status_code}')}

        logger.info(f'WhatsApp enviado para {number} (id={data.get("id")})')
        return {'status': 'sent', 'message': f'Relatorio enviado para {number}', 'response': data}

    except Exception as ex:
        logger.error(f'Erro ao chamar wweb.js: {ex}')
        return {'status': 'error', 'message': str(ex)}
