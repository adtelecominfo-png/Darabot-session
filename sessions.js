/**
 * In-memory session store shared between QR and Pair routes.
 * Each entry is keyed by a random session key and holds:
 *   { encoded, decoded, createdAt }
 * Entries are auto-expired after 10 minutes.
 */

const store = new Map();
const TTL_MS = 10 * 60 * 1000;

function set(key, encoded, decoded) {
  store.set(key, { encoded, decoded, createdAt: Date.now() });
}

function get(key) {
  return store.get(key) || null;
}

function del(key) {
  store.delete(key);
}

// GC every 2 minutes
setInterval(() => {
  const now = Date.now();
  for (const [k, v] of store.entries()) {
    if (now - v.createdAt > TTL_MS) store.delete(k);
  }
}, 2 * 60 * 1000);

module.exports = { set, get, del };
