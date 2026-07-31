const { makeid } = require('./gen-id');
const express = require('express');
const fs = require('fs');
const path = require('path');
const pino = require('pino');
const sessions = require('./sessions');
const {
  default: makeWASocket,
  useMultiFileAuthState,
  fetchLatestBaileysVersion,
  delay,
  Browsers,
  makeCacheableSignalKeyStore
} = require('@whiskeysockets/baileys');

const router = express.Router();

// In-memory QR state: key → { qr, status, message }
const qrStore = new Map();
const QR_TTL_MS = 5 * 60 * 1000;

function cleanup(key, tempDir) {
  qrStore.delete(key);
  try {
    if (fs.existsSync(tempDir)) fs.rmSync(tempDir, { recursive: true, force: true });
  } catch (_) {}
}

// POST /qr/start — kick off a QR session
router.post('/start', async (req, res) => {
  const key = makeid(10);
  const tempDir = path.join(__dirname, 'temp', key);

  qrStore.set(key, { status: 'pending', qr: null, message: null });

  // Auto-expire
  setTimeout(() => {
    if (qrStore.has(key)) cleanup(key, tempDir);
  }, QR_TTL_MS);

  res.json({ sessionKey: key });

  // Run connection in background
  startQRSession(key, tempDir).catch((err) => {
    const entry = qrStore.get(key);
    if (entry) qrStore.set(key, { ...entry, status: 'error', message: err.message });
  });
});

// GET /qr/poll/:key — frontend polls this
router.get('/poll/:key', (req, res) => {
  const { key } = req.params;
  const entry = qrStore.get(key);
  if (!entry) return res.json({ status: 'expired' });

  if (entry.status === 'done') {
    // Also return session data
    const sess = sessions.get(key);
    return res.json({
      status: 'done',
      encoded: sess ? sess.encoded : null,
      decoded: sess ? sess.decoded : null
    });
  }

  res.json(entry);
});

async function startQRSession(key, tempDir) {
  let sessionDone = false;

  const { state, saveCreds } = await useMultiFileAuthState(tempDir);
  const logger = pino({ level: 'fatal' }).child({ level: 'fatal' });
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    auth: {
      creds: state.creds,
      keys: makeCacheableSignalKeyStore(state.keys, logger)
    },
    printQRInTerminal: false,
    generateHighQualityLinkPreview: false,
    logger,
    syncFullHistory: false,
    browser: Browsers.ubuntu('Chrome'),
    keepAliveIntervalMs: 10000,
    connectTimeoutMs: 60000,
  });

  sock.ev.on('creds.update', saveCreds);

  // Capture QR code string
  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      // Coerce QR payload to a trimmed string to ensure frontend always receives a clean value.
      // Sometimes the library may emit a Buffer or include whitespace/newlines.
      let qrStr = null;
      try {
        if (typeof qr === 'string') qrStr = qr.trim();
        else if (qr && typeof qr.toString === 'function') qrStr = qr.toString().trim();
        else qrStr = String(qr).trim();
      } catch (_) {
        qrStr = null;
      }

      qrStore.set(key, { status: 'qr', qr: qrStr, message: null });
    }

    if (connection === 'open') {
      if (sessionDone) return;
      sessionDone = true;
      qrStore.set(key, { status: 'connected', qr: null, message: null });

      await delay(4000);

      try {
        const credsPath = path.join(tempDir, 'creds.json');
        const sessionData = fs.readFileSync(credsPath, 'utf8');
        const encoded = Buffer.from(sessionData).toString('base64');
        const decoded = sessionData; // raw JSON string

        // Store for download
        sessions.set(key, encoded, decoded);

        // Mark done
        qrStore.set(key, { status: 'done', qr: null, message: null });

        // Also send via WhatsApp
        await sock.sendMessage(sock.user.id, {
          text:
            `🤖 *DARATECH BOT — Session ID*\n\n` +
            `\`\`\`${encoded}\`\`\`\n\n` +
            `⚠️ *Never share this with anyone.*\n\n` +
            `📋 Copy the code above and paste it as your\n` +
            `SESSION_ID= in your bot's .env file.\n\n` +
            `_Powered by Daratech Bot_`
        });

        console.log(`✅ QR session created for ${sock.user.id}`);
      } catch (err) {
        console.error('QR session send error:', err.message);
        qrStore.set(key, { status: 'error', qr: null, message: 'Session created but send failed.' });
      } finally {
        await delay(1500);
        try { await sock.ws.close(); } catch (_) {}
        // keep tempDir briefly for download, cleanup handled by sessions TTL
        setTimeout(() => cleanup(key, tempDir), QR_TTL_MS);
      }

    } else if (connection === 'close') {
      const code = lastDisconnect?.error?.output?.statusCode;
      if (code === 401) {
        cleanup(key, tempDir);
      } else if (!sessionDone) {
        await delay(2000);
        // QR expired — let client know they need to restart
        const entry = qrStore.get(key);
        if (entry && entry.status !== 'done') {
          qrStore.set(key, { status: 'pending', qr: null, message: null });
        }
      }
    }
  });
}

module.exports = router;
