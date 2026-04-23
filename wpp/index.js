import express from 'express';
import qrcode from 'qrcode-terminal';
import QRCode from 'qrcode';
import whatsappWeb from 'whatsapp-web.js';

const { Client, LocalAuth } = whatsappWeb;

const PORT = process.env.PORT || 3001;
const CLIENT_ID = process.env.WPP_CLIENT_ID || 'openclaw';

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

function normalizeNumber(raw) {
    const digits = String(raw).replace(/\D/g, '');
    if (!digits) throw new Error('numero invalido');
    return digits.includes('@') ? digits : `${digits}@c.us`;
}

const app = express();
app.use(express.json({ limit: '1mb' }));

app.get('/qr', async (req, res) => {
    if (state.ready) return res.status(200).send('<h1>Ja conectado ao WhatsApp</h1>');
    if (!state.qr) return res.status(503).send('<h1>Aguardando QR... recarregue em alguns segundos</h1>');
    const dataUrl = await QRCode.toDataURL(state.qr, { width: 400, margin: 2 });
    res.send(`<!doctype html><html><body style="font-family:sans-serif;text-align:center;padding:40px">
        <h2>Escaneie o QR no WhatsApp do diretor</h2>
        <img src="${dataUrl}" alt="qr"/>
        <p>Recarregue a pagina apos escanear.</p>
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
