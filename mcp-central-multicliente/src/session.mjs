export class SessionStore {
  constructor() { this.sessions = new Map(); }

  select(sessionId, clientId) { this.sessions.set(sessionId, clientId); }
  get(sessionId) { return this.sessions.get(sessionId) || null; }
  clear(sessionId) { this.sessions.delete(sessionId); }
}
