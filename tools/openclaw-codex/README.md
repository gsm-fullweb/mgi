# OpenClaw + Codex (assinatura ChatGPT) no Windows

## Por que o OpenClaw "não consegue usar o Codex"

Nas versões atuais do OpenClaw:

| Causa | Sintoma | Correção |
|---|---|---|
| Login feito só no **Codex CLI** (`~/.codex`) | `No auth profile` / `Unknown model` | O OpenClaw **não importa mais** esse login. É preciso logar dentro do OpenClaw: `openclaw models auth login --provider openai` |
| Config antiga com `openai-codex/...`, `codex/...` ou `codex-cli/...` | Modelo não encontrado | `openclaw doctor --fix` (reescreve para `openai/...`) |
| Plugin `codex` desativado ou `plugins.allow` sem `codex`/`openai` | `/codex status` não responde | `openclaw config set plugins.entries.codex.enabled true` e incluir `codex` e `openai` no `plugins.allow` |
| Callback do navegador bloqueado (VPS, RDP, firewall) | Login trava no localhost | Use `--device-code` |
| Modelo que a conta não possui | `Unknown model` | `openclaw models list --provider openai` e escolha um da lista |

> Não existe mais provider `openai-codex`. O provider é **`openai`** e a rota é `openai/<modelo>`. O runtime Codex é escolhido automaticamente quando você está logado com a conta ChatGPT.

## Instalação rápida (recomendado)

PowerShell (não precisa ser admin):

```powershell
cd tools\openclaw-codex
powershell -ExecutionPolicy Bypass -File .\instalar-openclaw-codex.ps1
```

Opções:

```powershell
# navegador não volta pro localhost:
.\instalar-openclaw-codex.ps1 -DeviceCode
# escolher outro modelo:
.\instalar-openclaw-codex.ps1 -Model openai/gpt-5.5
# já logado, só corrigir config:
.\instalar-openclaw-codex.ps1 -SkipLogin
```

## Passo a passo manual

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex        # instala/atualiza
openclaw doctor --fix                                  # migra rotas legadas
openclaw config set plugins.entries.codex.enabled true
openclaw models auth login --provider openai           # login ChatGPT (Plus/Pro/Business)
openclaw models list --provider openai                 # ver modelos da sua conta
openclaw config set agents.defaults.model.primary openai/gpt-6-astra
openclaw gateway restart
```

No chat: `/codex status`, `/codex models` e `/status` → deve aparecer `Runtime: OpenAI Codex`.

## Config final esperada (`~/.openclaw/openclaw.json`)

```json5
{
  plugins: { entries: { codex: { enabled: true } } },
  agents: { defaults: { model: { primary: "openai/gpt-6-astra" } } },
}
```

Com API key como reserva (usa a assinatura primeiro e cai para a API key quando estourar o limite):

```json5
{
  auth: { order: { openai: ["openai:seu-email@exemplo.com", "openai:api-key-backup"] } },
}
```

## Diagnóstico

```powershell
openclaw models status
openclaw models auth list --provider openai
openclaw config get agents.defaults.model --json
openclaw config get models.providers.openai.agentRuntime --json
openclaw models status --probe --probe-provider openai
```

Se copiou credenciais do Codex CLI para dentro do `codex-home` do agente, importe:

```powershell
openclaw migrate apply codex --from <codex-home> --agent <agent-id> --include-secrets --item auth:openai --yes
```

Fonte: https://docs.openclaw.ai/providers/openai/setup
