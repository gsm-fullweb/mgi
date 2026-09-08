import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { loadClients } from "./config.mjs";
import { ClientRegistry } from "./registry.mjs";
import { SessionStore } from "./session.mjs";
import { assertAllowed } from "./policy.mjs";
import { audit } from "./audit.mjs";
import { McpClientAdapter } from "./adapter.mjs";

const registry = new ClientRegistry(loadClients());
const sessions = new SessionStore();
const adapter = new McpClientAdapter();
const server = new McpServer({ name: "mcp-central-multicliente", version: "0.1.0" });

function sessionId(extra) { return extra?.sessionId || "default"; }
function selected(extra) {
  const id = sessions.get(sessionId(extra));
  if (!id) throw new Error("Nenhum cliente selecionado. Use select_client primeiro.");
  return registry.get(id);
}

server.tool("list_clients", "Lista clientes ativos sem expor credenciais.", {}, async () => ({
  content: [{ type: "text", text: JSON.stringify(registry.list()) }]
}));

server.tool("select_client", "Seleciona explicitamente o cliente da sessão.", {
  client_id: z.string(),
  session_id: z.string().optional()
}, async ({ client_id, session_id = "default" }) => {
  const client = registry.get(client_id);
  sessions.select(session_id, client.id);
  audit("select_client", { session_id, client_id: client.id, domain: client.domain });
  return { content: [{ type: "text", text: JSON.stringify({ selected: client.id, domain: client.domain }) }] };
});

server.tool("get_selected_client", "Mostra o cliente atualmente selecionado.", {
  session_id: z.string().optional()
}, async ({ session_id = "default" }) => {
  const client = selected({ sessionId: session_id });
  return { content: [{ type: "text", text: JSON.stringify({ id: client.id, name: client.name, domain: client.domain }) }] };
});

server.tool("clear_client", "Remove o cliente selecionado da sessão.", {
  session_id: z.string().optional()
}, async ({ session_id = "default" }) => {
  sessions.clear(session_id);
  audit("clear_client", { session_id });
  return { content: [{ type: "text", text: JSON.stringify({ cleared: true }) }] };
});

server.tool("execute_client_ability", "Executa uma habilidade Novamira no cliente selecionado.", {
  ability: z.string(),
  parameters: z.record(z.unknown()).default({}),
  session_id: z.string().optional()
}, async ({ ability, parameters, session_id = "default" }) => {
  const client = selected({ sessionId: session_id });
  assertAllowed(client, ability, parameters);
  audit("execute_client_ability", { session_id, client_id: client.id, domain: client.domain, ability });
  const result = await adapter.execute(client, ability, parameters);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
});

await server.connect(new StdioServerTransport());
