const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const configPath = path.join(dataDir, 'site-config.json');
const defaults = {
  siteName: 'DARATECH V2',
  tagline: 'Your session. Your control.',
  maintenance: false
};

if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
function read() {
  try { return { ...defaults, ...JSON.parse(fs.readFileSync(configPath, 'utf8')) }; }
  catch (_) { return { ...defaults }; }
}
function write(next) {
  const safe = {
    siteName: String(next.siteName || defaults.siteName).trim().slice(0, 60) || defaults.siteName,
    tagline: String(next.tagline || defaults.tagline).trim().slice(0, 120) || defaults.tagline,
    maintenance: Boolean(next.maintenance)
  };
  fs.writeFileSync(configPath, JSON.stringify(safe, null, 2) + '\n');
  return safe;
}
if (!fs.existsSync(configPath)) write(defaults);
module.exports = { read, write, defaults };
