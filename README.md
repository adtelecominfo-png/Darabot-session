# Daratech Bot — Session ID Generator

A web app that generates your WhatsApp `SESSION_ID` for Daratech Bot using phone-number pairing (no QR code needed).

---

## How It Works

1. User enters their WhatsApp number on the website
2. A pairing code is shown — they enter it in WhatsApp under **Linked Devices → Link with phone number**
3. The bot connects and sends the `SESSION_ID` directly to their own WhatsApp chat
4. User copies the `SESSION_ID` into their bot's `.env` file

---

## Deploy on Render

1. Push this `session_generator/` folder as its own GitHub repo (or use a sub-path deploy)
2. Create a new **Web Service** on [Render](https://render.com)
3. Set:
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
4. No environment variables needed — `PORT` is set by Render automatically
5. Done — your site is live

---

## Run Locally

```bash
cd session_generator
npm install
npm start
# Open http://localhost:3000
```

---

## Deploy Anywhere Else

The app only needs **Node.js 18+** and reads `PORT` from the environment (defaults to `3000`).

Works on: Render · Railway · Heroku · Koyeb · VPS

---

## Project Structure

```
session_generator/
├── index.js        → Express entry point
├── pair.js         → WhatsApp Baileys pairing logic
├── gen-id.js       → random temp-folder ID helper
├── public/
│   └── index.html  → frontend UI
├── package.json
├── .env.example
└── .gitignore
```

---

## Notes

- `SESSION_ID` generated here is plain base64 — compatible with Daratech Bot's `.env` format
- Each pairing creates a temp folder under `temp/` that is deleted automatically after the session is created
- The app does **not** store or log any session data
