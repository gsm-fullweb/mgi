# MCP Central Multi-Cliente

Gateway MCP para operar vários WordPress/Novamira com isolamento por cliente.

## Princípios

- Nenhuma operação de escrita ocorre sem um cliente selecionado na sessão.
- O domínio esperado é validado antes de encaminhar a chamada.
- Credenciais ficam fora do cadastro versionado, em variáveis de ambiente.
- Cada chamada gera um registro de auditoria sem expor tokens.
- Ações destrutivas exigem `confirm: true`.

## Estrutura

```text
src/
  config.mjs       carrega o cadastro e as variáveis de ambiente
  registry.mjs     valida e consulta clientes
  session.mjs      mantém o cliente selecionado por sessão
  policy.mjs       aplica as regras de segurança
  audit.mjs        registra operações sanitizadas
  adapter.mjs      contrato para o conector MCP de cada cliente
  server.mjs       ponto de entrada MCP e ferramentas expostas
config/
  clients.example.json
```

## Fluxo seguro

1. `list_clients` mostra apenas clientes ativos.
2. `select_client` fixa o cliente na sessão e retorna domínio e status.
3. `get_selected_client` confirma o contexto atual.
4. Operações de conteúdo exigem o contexto selecionado e são encaminhadas pelo adapter.
5. `clear_client` encerra o contexto antes de trocar de cliente.

## Próximo passo de integração

Preencha `config/clients.json` a partir do exemplo e configure um endpoint MCP para cada cliente. O adapter foi deixado como contrato explícito porque o endpoint Novamira de cada instalação deve ser conectado sem compartilhar tokens entre clientes.

## Execução

```powershell
npm install
npm start
```

O servidor usa transporte STDIO, adequado para ser registrado como um único servidor MCP no cliente agente.
