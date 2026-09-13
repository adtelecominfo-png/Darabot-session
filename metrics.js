const startedAt = Date.now();
const counters = {
  requests: 0,
  blockedRequests: 0,
  qrStarts: 0,
  pairStarts: 0,
  sessionsCreated: 0,
  errors: 0
};

function increment(name) {
  if (Object.prototype.hasOwnProperty.call(counters, name)) counters[name] += 1;
}

function snapshot() {
  return {
    uptimeSeconds: Math.floor((Date.now() - startedAt) / 1000),
    startedAt: new Date(startedAt).toISOString(),
    counters: { ...counters }
  };
}

module.exports = { increment, snapshot };
