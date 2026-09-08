export class McpClientAdapter {
  async execute(_client, _ability, _parameters) {
    throw new Error(
      "Adapter MCP ainda não configurado: conecte aqui o transporte do endpoint Novamira do cliente."
    );
  }
}
