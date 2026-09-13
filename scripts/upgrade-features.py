from pathlib import Path

path = Path('/home/ubuntu/Darabot-session/public/index.html')
html = path.read_text()

html = html.replace('''    .status-chip { display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: 12px; font-weight: 700; }''', '''    .top-actions { display: flex; align-items: center; gap: 9px; }
    .utility-btn, .language-select { border: 1px solid var(--line); border-radius: 10px; background: rgba(255,255,255,.72); color: var(--ink); font-size: 12px; font-weight: 800; padding: 9px 11px; }
    .utility-btn:hover, .language-select:hover { border-color: var(--green); color: var(--green-dark); }
    .language-select { cursor: pointer; }
    .status-chip { display: flex; align-items: center; gap: 8px; color: var(--muted); font-size: 12px; font-weight: 700; }
    body.dark { --ink: #e9f5ee; --muted: #9bb1a5; --paper: #0b1712; --card: rgba(18,35,27,.92); --line: #294438; --mint: #153a2a; --shadow: 0 24px 70px rgba(0,0,0,.25); }
    body.dark .utility-btn, body.dark .language-select, body.dark .phone-field, body.dark .session-value { background: #10241a; color: var(--ink); }
    body.dark .qr-stage { background: #10241a; border-color: #35664d; }
    body.dark .qr-wrap, body.dark .session-box { background: #10241a; }
    body.dark .session-value { border-color: var(--line); }
    .content-section { max-width: 850px; margin-top: 58px; }
    .content-section h2 { font-size: 26px; letter-spacing: -.05em; margin-bottom: 12px; }
    .content-section > p { color: var(--muted); line-height: 1.65; font-size: 14px; }
    .guide-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 18px; }
    .guide-card { padding: 18px; border: 1px solid var(--line); border-radius: 16px; background: var(--card); }
    .guide-card b { color: var(--green-dark); display: block; margin-bottom: 7px; }
    .guide-card p { color: var(--muted); font-size: 13px; line-height: 1.55; }
    .faq-list { display: grid; gap: 8px; margin-top: 18px; }
    .faq-list details { padding: 14px 16px; border: 1px solid var(--line); border-radius: 12px; background: var(--card); }
    .faq-list summary { cursor: pointer; font-size: 13px; font-weight: 900; }
    .faq-list p { color: var(--muted); font-size: 13px; line-height: 1.6; padding-top: 10px; }
    .timer { display: inline-flex; align-items: center; gap: 6px; margin-top: 15px; color: #9a661a; font-size: 12px; font-weight: 900; }
    .retry-btn { display: none; margin-top: 14px; border: 0; background: transparent; color: var(--danger); font-size: 13px; font-weight: 900; }
    .retry-btn.show { display: inline-block; }
    .install-banner { display: none; align-items: center; justify-content: space-between; gap: 15px; max-width: 850px; margin-top: 20px; padding: 14px 16px; border: 1px solid #b8e8ca; border-radius: 14px; background: var(--mint); color: var(--green-dark); font-size: 13px; font-weight: 800; }
    .install-banner.show { display: flex; }
    .install-banner button { border: 0; border-radius: 9px; padding: 9px 12px; background: var(--green-dark); color: white; font-size: 12px; font-weight: 900; }
    .status-panel { display: none; max-width: 850px; margin-top: 20px; padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: var(--card); }
    .status-panel.show { display: block; }
    .status-panel strong { display: block; margin-bottom: 5px; }
    .status-panel p { color: var(--muted); font-size: 13px; }
    .status-panel.ok strong { color: var(--green-dark); }
    .status-panel.fail strong { color: var(--danger); }
    .env-copy { margin-top: 10px; }
    .env-copy .backup-btn { margin-top: 0; }
    .visibility-btn { float: right; border: 0; background: transparent; color: var(--green-dark); font-size: 11px; font-weight: 900; }''')
html = html.replace('''      <div class="status-chip"><i class="status-dot"></i> Secure session generator</div>''', '''      <div class="top-actions"><button class="utility-btn" id="themeBtn" onclick="toggleTheme()" aria-label="Toggle dark mode">☾</button><select class="language-select" id="languageSelect" onchange="setLanguage(this.value)" aria-label="Language"><option value="en">EN</option><option value="fr">FR</option><option value="ha">HA</option></select><button class="utility-btn" onclick="checkStatus()">Status</button><div class="status-chip"><i class="status-dot"></i> Secure session generator</div></div>''')
html = html.replace('''        <div class="feature-strip"><span><b>✓</b> No session data stored</span><span><b>✓</b> Copy-ready output</span><span><b>✓</b> Works on mobile</span></div>''', '''        <div class="feature-strip"><span><b>✓</b> No session data stored</span><span><b>✓</b> Copy-ready output</span><span><b>✓</b> Works on mobile</span></div>
        <div class="install-banner" id="installBanner"><span>Install DARATECH V2 for faster access.</span><button onclick="installApp()">Install app</button></div>
        <div class="status-panel" id="statusPanel"></div>
        <section class="content-section" id="guide"><h2>How it works</h2><p>Choose a method, connect your WhatsApp, then copy the generated value into your bot environment.</p><div class="guide-grid"><div class="guide-card"><b>1 · Choose</b><p>Use QR for a camera scan or Pair Code when you prefer typing a short code.</p></div><div class="guide-card"><b>2 · Connect</b><p>Follow the WhatsApp prompts while this page keeps your connection active.</p></div><div class="guide-card"><b>3 · Copy</b><p>Copy the session ID and add it to your bot's <strong>SESSION_ID=</strong> variable.</p></div></div></section>
        <section class="content-section" id="faq"><h2>Common questions</h2><div class="faq-list"><details><summary>Is my session ID stored?</summary><p>No. The in-memory session record expires automatically and is never written to a database.</p></details><details><summary>Which method should I use?</summary><p>QR is fastest when you have access to your phone camera. Pair Code is useful when scanning is inconvenient.</p></details><details><summary>What if the code expires?</summary><p>Start again and generate a fresh QR or Pair Code. Old temporary files are cleaned up automatically.</p></details></div></section>''')
html = html.replace('''<div class="qr-stage"><div class="qr-wrap"><div class="qr-placeholder" id="qrPlaceholder"><span class="spinner" style="width:28px;height:28px"></span><span>Creating your QR code…</span></div><canvas id="qrCanvas" style="display:none"></canvas></div></div>''', '''<div class="qr-stage"><div class="qr-wrap"><div class="qr-placeholder" id="qrPlaceholder"><span class="spinner" style="width:28px;height:28px"></span><span>Creating your QR code…</span></div><canvas id="qrCanvas" style="display:none"></canvas></div></div><div class="timer" id="qrTimer">⏱ QR expires in 60s</div><button class="retry-btn" id="qrRetryBtn" onclick="resetQR()">QR expired — generate a new one</button>''')
html = html.replace('''<div class="session-box"><div class="session-box-head"><span>SESSION_ID</span><span>Base64</span></div><textarea class="session-value" id="qrSessionValue" readonly placeholder="Preparing…"></textarea><button class="copy-btn" id="qrCopyBtn" onclick="copySession('qr')">Copy SESSION_ID</button><button class="backup-btn" onclick="downloadSession('qr')">Download a backup file</button></div>''', '''<div class="session-box"><div class="session-box-head"><span>SESSION_ID</span><span>Base64 <button class="visibility-btn" onclick="toggleSecret('qrSessionValue', this)">Hide</button></span></div><textarea class="session-value" id="qrSessionValue" readonly placeholder="Preparing…"></textarea><button class="copy-btn" id="qrCopyBtn" onclick="copySession('qr')">Copy SESSION_ID</button><div class="env-copy"><button class="backup-btn" onclick="copyEnv('qr')">Copy SESSION_ID= variable</button></div><button class="backup-btn" onclick="downloadSession('qr')">Download a backup file</button></div>''')
html = html.replace('''<div class="session-box"><div class="session-box-head"><span>SESSION_ID</span><span>Base64</span></div><textarea class="session-value" id="pairSessionValue" readonly placeholder="Preparing…"></textarea><button class="copy-btn" id="pairCopyBtn" onclick="copySession('pair')">Copy SESSION_ID</button><button class="backup-btn" onclick="downloadSession('pair')">Download a backup file</button></div>''', '''<div class="session-box"><div class="session-box-head"><span>SESSION_ID</span><span>Base64 <button class="visibility-btn" onclick="toggleSecret('pairSessionValue', this)">Hide</button></span></div><textarea class="session-value" id="pairSessionValue" readonly placeholder="Preparing…"></textarea><button class="copy-btn" id="pairCopyBtn" onclick="copySession('pair')">Copy SESSION_ID</button><div class="env-copy"><button class="backup-btn" onclick="copyEnv('pair')">Copy SESSION_ID= variable</button></div><button class="backup-btn" onclick="downloadSession('pair')">Download a backup file</button></div>''')
html = html.replace('''    let qrSessionKey = null, qrPollTimer = null, qrEncoded = '';
    let pairSessionKey = null, pairPollTimer = null, pairEncoded = '';''', '''    let qrSessionKey = null, qrPollTimer = null, qrEncoded = '', qrSeconds = 60, qrTimer = null;
    let pairSessionKey = null, pairPollTimer = null, pairEncoded = '';
    let deferredInstallPrompt = null;
    const translations = { en: { hero: 'WhatsApp connection made simple', copy: 'Generate a secure DARATECH V2 session ID in seconds. Choose the connection method that works best for you.' }, fr: { hero: 'Connexion WhatsApp simplifiée', copy: 'Générez votre identifiant de session DARATECH V2 en quelques secondes.' }, ha: { hero: 'Haɗin WhatsApp cikin sauƙi', copy: 'Ƙirƙiri session ID na DARATECH V2 cikin daƙiƙu.' } };''')
html = html.replace('''    function goLanding() { stopQRPoll(); stopPairPoll(); qrSessionKey = null; qrEncoded = ''; pairSessionKey = null; pairEncoded = ''; showView('view-landing'); }''', '''    function goLanding() { stopQRPoll(); stopPairPoll(); stopQRCountdown(); qrSessionKey = null; qrEncoded = ''; pairSessionKey = null; pairEncoded = ''; showView('view-landing'); }''')
html = html.replace('''    function resetQR() { stopQRPoll(); qrSessionKey = null; qrEncoded = ''; resetQRCards(); }''', '''    function resetQR() { stopQRPoll(); stopQRCountdown(); qrSessionKey = null; qrEncoded = ''; resetQRCards(); document.getElementById('qrRetryBtn').classList.remove('show'); }''')
html = html.replace('''qrSessionKey = d.sessionKey; showQRCard('qr-step2'); startQRPoll();''', '''qrSessionKey = d.sessionKey; showQRCard('qr-step2'); startQRCountdown(); startQRPoll();''')
html = html.replace('''else if (d.status === 'expired') { stopQRPoll(); resetQR(); setStatus('qrStatusBox','This session expired. Please start again.','error'); } else if (d.status === 'error') { stopQRPoll(); resetQR(); setStatus('qrStatusBox',d.message || 'Something went wrong.','error'); }''', '''else if (d.status === 'expired') { stopQRPoll(); stopQRCountdown(); document.getElementById('qrRetryBtn').classList.add('show'); showQRLoading('QR expired. Generate a new one.'); } else if (d.status === 'error') { stopQRPoll(); stopQRCountdown(); document.getElementById('qrRetryBtn').classList.add('show'); showQRLoading(d.message || 'Something went wrong.'); }''')
html = html.replace('''function showQRLoading(msg) { const p=document.getElementById('qrPlaceholder'), c=document.getElementById('qrCanvas');''', '''function startQRCountdown() { stopQRCountdown(); qrSeconds = 60; updateQRCountdown(); qrTimer = setInterval(() => { qrSeconds -= 1; updateQRCountdown(); if (qrSeconds <= 0) { stopQRCountdown(); document.getElementById('qrRetryBtn').classList.add('show'); } }, 1000); }
    function stopQRCountdown() { if (qrTimer) { clearInterval(qrTimer); qrTimer = null; } }
    function updateQRCountdown() { const el = document.getElementById('qrTimer'); if (el) el.textContent = qrSeconds > 0 ? '⏱ QR expires in ' + qrSeconds + 's' : '⏱ QR expired'; }
    function showQRLoading(msg) { const p=document.getElementById('qrPlaceholder'), c=document.getElementById('qrCanvas');''')
html = html.replace('''    function downloadSession(flow) {''', '''    async function copyEnv(flow) { const value = flow === 'qr' ? qrEncoded : pairEncoded; if (value) await navigator.clipboard.writeText('SESSION_ID=' + value); }
    function toggleSecret(id, button) { const area = document.getElementById(id); area.dataset.hidden = area.dataset.hidden !== 'true' ? 'true' : 'false'; if (area.dataset.hidden === 'true') { area.dataset.real = area.value; area.value = '•'.repeat(Math.min(area.dataset.real.length, 180)); button.textContent = 'Show'; } else { area.value = area.dataset.real || area.value; button.textContent = 'Hide'; } }
    function downloadSession(flow) {''')
html = html.replace('''    document.getElementById('phoneInput').addEventListener('keydown',e=>{if(e.key==='Enter')getCode();});''', '''    document.getElementById('phoneInput').addEventListener('keydown',e=>{if(e.key==='Enter')getCode();});
    function toggleTheme() { document.body.classList.toggle('dark'); localStorage.setItem('daratech-theme', document.body.classList.contains('dark') ? 'dark' : 'light'); document.getElementById('themeBtn').textContent = document.body.classList.contains('dark') ? '☀' : '☾'; }
    function setLanguage(lang) { localStorage.setItem('daratech-language', lang); const t = translations[lang] || translations.en; document.querySelector('.eyebrow').textContent = t.hero; document.querySelector('.hero-copy').textContent = t.copy; }
    async function checkStatus() { const panel = document.getElementById('statusPanel'); panel.className = 'status-panel show'; panel.innerHTML = '<strong>Checking service…</strong><p>Please wait.</p>'; try { const data = await (await fetch('/status')).json(); panel.className = 'status-panel show ok'; panel.innerHTML = '<strong>✓ Service operational</strong><p>' + data.message + '</p>'; } catch (_) { panel.className = 'status-panel show fail'; panel.innerHTML = '<strong>Service unavailable</strong><p>Try again in a moment.</p>'; } }
    window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); deferredInstallPrompt = e; document.getElementById('installBanner').classList.add('show'); });
    async function installApp() { if (!deferredInstallPrompt) return; deferredInstallPrompt.prompt(); await deferredInstallPrompt.userChoice; deferredInstallPrompt = null; document.getElementById('installBanner').classList.remove('show'); }
    if (localStorage.getItem('daratech-theme') === 'dark') toggleTheme();
    setLanguage(localStorage.getItem('daratech-language') || 'en');''')
path.write_text(html)
print('Frontend feature migration complete')
