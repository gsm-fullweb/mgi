import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const file = process.env.CLIENTS_CONFIG || path.join(root, "config", "clients.json");

export function loadClients() {
  if (!fs.existsSync(file)) {
    throw new Error(`Cadastro de clientes não encontrado: ${file}`);
  }
  const clients = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!Array.isArray(clients)) throw new Error("O cadastro deve ser um array JSON.");
  return clients.map((client) => {
    if (!/^[a-z0-9-]+$/.test(client.id || "")) throw new Error(`ID inválido: ${client.id}`);
    if (!client.domain || !client.mcpEndpointEnv || !client.mcpTokenEnv) {
      throw new Error(`Cadastro incompleto para ${client.id}`);
    }
    return {
      ...client,
      endpoint: process.env[client.mcpEndpointEnv] || "",
      token: process.env[client.mcpTokenEnv] || ""
    };
  });
}
