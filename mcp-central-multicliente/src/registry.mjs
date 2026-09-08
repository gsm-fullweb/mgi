export class ClientRegistry {
  constructor(clients) {
    this.clients = new Map(clients.map((client) => [client.id, client]));
  }

  list() {
    return [...this.clients.values()]
      .filter((client) => client.active !== false)
      .map(({ id, name, domain, active }) => ({ id, name, domain, active }));
  }

  get(id) {
    const client = this.clients.get(id);
    if (!client || client.active === false) throw new Error(`Cliente indisponível: ${id}`);
    return client;
  }
}
