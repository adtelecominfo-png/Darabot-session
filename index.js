require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const sessions = require('./sessions');

const app = express();
const pairRouter = require('./pair');
const qrRouter = require('./qr');

const PORT = process.env.PORT || 3000;

// Ensure temp dir exists
const tempDir = path.join(__dirname, 'temp');
if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });

app.use(cors());
app.use(express.json());

// ── API routes ──────────────────────────────────────────────
// Pairing code flow
app.use('/code', pairRouter);

// QR code flow
app.use('/qr', qrRouter);

// Download session file
// GET /download/:key?type=encoded|decoded
app.get('/download/:key', (req, res) => {
  const { key } = req.params;
  const type = (req.query.type || 'encoded').toLowerCase();
  const sess = sessions.get(key);

  if (!sess) {
    return res.status(404).json({ error: 'Session not found or expired.' });
  }

  let content, filename;

  if (type === 'decoded') {
    // Pretty-print the raw JSON
    try {
      content = JSON.stringify(JSON.parse(sess.decoded), null, 2);
    } catch (_) {
      content = sess.decoded;
    }
    filename = `daratech-session-decoded-${key}.txt`;
  } else {
    // Encoded base64 — ready to paste as SESSION_ID
    content =
      `DARATECH BOT — SESSION ID (Encoded / Base64)\n` +
      `============================================\n` +
      `Generated: ${new Date().toUTCString()}\n\n` +
      `Paste this value into your .env file:\n` +
      `SESSION_ID=${sess.encoded}\n\n` +
      `⚠ Never share this file with anyone.\n` +
      `⚠ It gives full access to your WhatsApp account.\n`;
    filename = `daratech-session-encoded-${key}.txt`;
  }

  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
  res.send(content);
});

// ── Frontend ─────────────────────────────────────────────────
app.use(express.static(path.join(__dirname, 'public')));
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`✅ Daratech Session Generator running on port ${PORT}`);
});

module.exports = app;
