import express from 'express';
import qrcode from 'qrcode-terminal';
import QRCode from 'qrcode';
import whatsappWeb from 'whatsapp-web.js';

const { Client, LocalAuth, MessageMedia } = whatsappWeb;

const PORT = process.env.PORT || 3001;
const CLIENT_ID = process.env.WPP_CLIENT_ID || 'openclaw';
const BACKEND_URL = process.env.BACKEND_URL || 'http://openclaw-backend:8000';
const ALLOWED_SENDERS = (process.env.ALLOWED_SENDERS || '').split(',').map(s => s.trim()).filter(Boolean);

const state = {
    ready: false,
    qr: null,
    lastError: null,
};

const client = new Client({
    authStrategy: new LocalAuth({ clientId: CLIENT_ID }),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
        ],
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/google-chrome',
    },
});

client.on('qr', (qr) => {
    state.qr = qr;
    state.ready = false;
    console.log('\n' + '='.repeat(80));
    console.log('QR CODE GERADO - Escaneie com o WhatsApp do diretor:');
    console.log('='.repeat(80));
    qrcode.generate(qr, { small: true });
    console.log('='.repeat(80) + '\n');
});

client.on('authenticated', () => {
    console.log('[WPP] Autenticado com sucesso.');
    state.qr = null;
});

client.on('auth_failure', (msg) => {
    console.error('[WPP] Falha de autenticacao:', msg);
    state.lastError = `auth_failure: ${msg}`;
});

client.on('ready', () => {
    console.log('[WPP] Cliente pronto. WhatsApp conectado.');
    state.ready = true;
    state.qr = null;
});

client.on('disconnected', (reason) => {
    console.log('[WPP] Desconectado:', reason);
    state.ready = false;
    state.lastError = `disconnected: ${reason}`;
    client.initialize();
});

client.on('message', async (message) => {
    try {
        if (message.fromMe) return;
        if (message.from.endsWith('@g.us')) return;
        if (message.from === 'status@broadcast') return;
        if (message.type !== 'chat' || !message.body) return;

        if (ALLOWED_SENDERS.length > 0) {
            const digits = message.from.replace(/\D/g, '');
            const allowed = ALLOWED_SENDERS.some(a => digits.includes(a.replace(/\D/g, '')));
            if (!allowed) {
                console.log(`[WPP] ignorando remetente nao autorizado: ${message.from}`);
                return;
            }
        }

        console.log(`[WPP] <- ${message.from}: ${message.body.slice(0, 120)}`);
        const chat = await message.getChat();
        await chat.sendStateTyping();

        const res = await fetch(`${BACKEND_URL}/api/v1/chat/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: message.from, text: message.body }),
        });

        if (!res.ok) {
            const txt = await res.text();
            console.error(`[WPP] backend ${res.status}: ${txt}`);
            await message.reply('Desculpe, tive um problema pra responder. Tenta de novo em instantes.');
            return;
        }

        const { reply, attachments = [] } = await res.json();
        if (reply) await message.reply(reply);
        for (const att of attachments) {
            try {
                const media = new MessageMedia(att.mime_type, att.data_base64, att.filename);
                await chat.sendMessage(media, { sendMediaAsDocument: true, caption: att.filename });
                console.log(`[WPP] -> ${message.from}: anexo ${att.filename} (${att.mime_type})`);
            } catch (e) {
                console.error('[WPP] erro ao enviar anexo:', e);
            }
        }
        console.log(`[WPP] -> ${message.from}: ${(reply || '').slice(0, 120)}`);
    } catch (ex) {
        console.error('[WPP] erro no handler de mensagem:', ex);
        try { await message.reply('Erro interno. Tenta de novo.'); } catch {}
    }
});

function normalizeNumber(raw) {
    const digits = String(raw).replace(/\D/g, '');
    if (!digits) throw new Error('numero invalido');
    return digits.includes('@') ? digits : `${digits}@c.us`;
}

const app = express();
app.use(express.json({ limit: '1mb' }));

app.get('/qr.png', async (req, res) => {
    if (!state.qr) return res.status(404).end();
    const buf = await QRCode.toBuffer(state.qr, { width: 400, margin: 2 });
    res.set('Content-Type', 'image/png');
    res.set('Cache-Control', 'no-store');
    res.send(buf);
});

app.get('/qr', (req, res) => {
    const baseStyle = 'font-family:sans-serif;text-align:center;padding:40px;background:#111;color:#eee';
    if (state.ready) {
        return res.send(`<!doctype html><html><head><meta charset="utf-8"><title>OpenClaw WhatsApp</title></head>
        <body style="${baseStyle}">
            <h2>WhatsApp conectado</h2>
            <p>Pronto para enviar mensagens.</p>
        </body></html>`);
    }
    const qrSrc = state.qr ? `/qr.png?t=${Date.now()}` : '';
    res.send(`<!doctype html><html><head><meta charset="utf-8"><title>OpenClaw WhatsApp</title></head>
    <body style="${baseStyle}">
        <h2 id="title">${state.qr ? 'Escaneie o QR no WhatsApp do diretor' : 'Gerando QR code...'}</h2>
        <img id="qr" src="${qrSrc}" style="background:#fff;padding:16px;border-radius:8px;${state.qr ? '' : 'display:none'}" alt=""/>
        <p id="info">${state.qr ? 'A pagina atualiza sozinha.' : 'Aguarde alguns segundos.'}</p>
        <script>
        async function tick(){
            try {
                const r = await fetch('/status'); const s = await r.json();
                if (s.ready) {
                    document.getElementById('title').textContent = 'WhatsApp conectado';
                    document.getElementById('qr').style.display = 'none';
                    document.getElementById('info').textContent = 'Pronto para enviar mensagens.';
                    return;
                }
                if (s.waiting_qr) {
                    const img = document.getElementById('qr');
                    img.style.display = '';
                    img.src = '/qr.png?t=' + Date.now();
                    document.getElementById('title').textContent = 'Escaneie o QR no WhatsApp do diretor';
                    document.getElementById('info').textContent = 'A pagina atualiza sozinha.';
                }
            } catch(e) {}
            setTimeout(tick, 3000);
        }
        tick();
        </script>
    </body></html>`);
});

app.get('/status', (req, res) => {
    res.json({
        ready: state.ready,
        waiting_qr: Boolean(state.qr),
        last_error: state.lastError,
    });
});

app.post('/send-message', async (req, res) => {
    const { number, text } = req.body || {};
    if (!number || !text) {
        return res.status(400).json({ status: 'error', message: 'number e text sao obrigatorios' });
    }
    if (!state.ready) {
        return res.status(503).json({ status: 'error', message: 'cliente WhatsApp ainda nao conectado' });
    }
    try {
        const chatId = normalizeNumber(number);
        const msg = await client.sendMessage(chatId, text);
        console.log(`[WPP] Mensagem enviada para ${chatId} (id=${msg.id?._serialized})`);
        return res.json({ status: 'sent', to: chatId, id: msg.id?._serialized });
    } catch (ex) {
        console.error('[WPP] Erro ao enviar:', ex);
        return res.status(500).json({ status: 'error', message: ex.message });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`[WPP] API ouvindo em :${PORT}`);
});

client.initialize();
