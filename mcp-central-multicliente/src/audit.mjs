export function audit(event, data = {}) {
  const safe = { ...data };
  delete safe.token;
  delete safe.authorization;
  console.error(JSON.stringify({
    time: new Date().toISOString(),
    event,
    ...safe
  }));
}
