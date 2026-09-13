require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const sessions = require('./sessions');
const metrics = require('./metrics');

const app = express();
const pairRouter = require('./pair');
const qrRouter = require('./qr');
const PORT = process.env.PORT || 3000;
const tempDir = path.join(__dirname, 'temp');
const rateWindowMs = 60 * 1000;
const rateLimit = 12;
const requestBuckets = new Map();

if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });
app.set('trust proxy', 1);
app.use((req, res, next) => {
  metrics.increment('requests');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'");
  if (req.secure || req.headers['x-forwarded-proto'] === 'https') res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
app.use(cors());
app.use(express.json({ limit: '32kb' }));

function clientIp(req) {
  return String(req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown').split(',')[0].trim();
}
function throttlePairing(req, res, next) {
  if (req.path.startsWith('/poll/')) return next();
  const key = `${clientIp(req)}:${req.baseUrl === '/qr' ? 'qr' : 'pair'}`;
  const now = Date.now();
  const recent = (requestBuckets.get(key) || []).filter(timestamp => now - timestamp < rateWindowMs);
  if (recent.length >= rateLimit) {
    metrics.increment('blockedRequests');
    res.setHeader('Retry-After', '60');
    return res.status(429).json({ error: 'Too many attempts. Please wait a minute and try again.' });
  }
  recent.push(now);
  requestBuckets.set(key, recent);
  next();
}

app.get('/healthz', (req, res) => res.json({ ok: true, service: 'DARATECH V2', uptime: metrics.snapshot().uptimeSeconds }));
app.get('/status', (req, res) => res.json({ ok: true, service: 'DARATECH V2', message: 'Pairing service is operational.', checkedAt: new Date().toISOString() }));
app.get('/admin/metrics', (req, res) => {
  const token = process.env.ADMIN_TOKEN;
  if (!token || req.get('authorization') !== `Bearer ${token}`) return res.status(404).json({ error: 'Not found' });
  res.json(metrics.snapshot());
});

app.use('/code', throttlePairing, pairRouter);
app.use('/qr', throttlePairing, qrRouter);

app.get('/download/:key', (req, res) => {
  const { key } = req.params;
  const type = (req.query.type || 'encoded').toLowerCase();
  const sess = sessions.get(key);
  if (!sess) return res.status(404).json({ error: 'Session not found or expired.' });
  let content, filename;
  if (type === 'decoded') {
    try { content = JSON.stringify(JSON.parse(sess.decoded), null, 2); } catch (_) { content = sess.decoded; }
    filename = `daratech-session-decoded-${key}.txt`;
  } else {
    content = `DARATECH V2 — SESSION ID (Encoded / Base64)\n============================================\nGenerated: ${new Date().toUTCString()}\n\nPaste this value into your .env file:\nSESSION_ID=${sess.encoded}\n\n⚠ Never share this file with anyone.\n⚠ It gives full access to your WhatsApp account.\n`;
    filename = `daratech-session-encoded-${key}.txt`;
  }
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
  res.send(content);
});

app.use(express.static(path.join(__dirname, 'public'), { maxAge: '1h' }));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));

const cleanupTemp = () => {
  const cutoff = Date.now() - 20 * 60 * 1000;
  try {
    for (const entry of fs.readdirSync(tempDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const folder = path.join(tempDir, entry.name);
      if (fs.statSync(folder).mtimeMs < cutoff) fs.rmSync(folder, { recursive: true, force: true });
    }
  } catch (error) { console.error('Temp cleanup error:', error.message); }
};
setInterval(cleanupTemp, 10 * 60 * 1000).unref();
cleanupTemp();

app.listen(PORT, () => console.log(`✅ DARATECH V2 running on port ${PORT}`));
module.exports = app;
