<#
.SYNOPSIS
  Instala/atualiza o OpenClaw e conecta o Codex (assinatura ChatGPT) no Windows.

.DESCRIPTION
  Corrige os casos mais comuns em que o OpenClaw "nao consegue usar o Codex":
    1. OpenClaw desatualizado (rotas antigas openai-codex/* e codex/*).
    2. Login feito so no Codex CLI (~/.codex) - o OpenClaw NAO importa mais esse login.
    3. Plugin "codex" desativado ou fora de plugins.allow.
    4. Modelo padrao apontando para uma rota legada.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\instalar-openclaw-codex.ps1
  powershell -ExecutionPolicy Bypass -File .\instalar-openclaw-codex.ps1 -DeviceCode
  powershell -ExecutionPolicy Bypass -File .\instalar-openclaw-codex.ps1 -Model openai/gpt-5.5
#>
param(
  # Modelo padrao. Se sua conta nao expuser este, o script lista os disponiveis.
  [string]$Model = "openai/gpt-6-astra",
  # Use quando o navegador nao consegue voltar para o localhost (VPS, RDP, firewall).
  [switch]$DeviceCode,
  # Pula o login (ja autenticado).
  [switch]$SkipLogin
)

$ErrorActionPreference = "Stop"
function Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Has($cmd)  { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# 1. Node.js (OpenClaw exige Node 24.16+ ou 26.1+)
Step "Verificando Node.js"
if (Has node) {
  $v = (node -v).TrimStart("v").Split(".")
  $major = [int]$v[0]; $minor = [int]$v[1]
  $ok = ($major -ge 27) -or ($major -eq 26 -and $minor -ge 1) -or ($major -eq 24 -and $minor -ge 16) -or ($major -eq 25)
  if (-not $ok) { Write-Warning "Node $(node -v) e antigo. O instalador oficial vai cuidar disso." }
} else {
  Write-Host "Node nao encontrado - o instalador oficial instala automaticamente."
}

# 2. Instalar ou atualizar o OpenClaw (instalador oficial, sem onboarding interativo)
Step "Instalando/atualizando OpenClaw"
& ([scriptblock]::Create((Invoke-WebRequest -UseBasicParsing https://openclaw.ai/install.ps1))) -NoOnboard
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
if (-not (Has openclaw)) { throw "openclaw nao esta no PATH. Feche e abra o PowerShell e rode o script de novo." }
openclaw --version

# 3. Migrar config legada (openai-codex/*, codex/*, codex-cli/*) para openai/*
Step "Corrigindo configuracao legada (doctor --fix)"
openclaw doctor --fix
openclaw config validate

# 4. Garantir o plugin nativo do Codex
Step "Ativando plugin codex"
openclaw config set plugins.entries.codex.enabled true
$allow = openclaw config get plugins.allow --json 2>$null
if ($allow -and $allow -ne "null" -and $allow -notmatch '"codex"') {
  Write-Warning "plugins.allow esta definido e NAO contem 'codex' (nem talvez 'openai'). Adicione ambos: $allow"
}

# 5. Login OAuth com a conta ChatGPT (Plus/Pro/Business) - o login do Codex CLI nao e reaproveitado
if (-not $SkipLogin) {
  Step "Login ChatGPT/Codex no OpenClaw"
  if ($DeviceCode) { openclaw models auth login --provider openai --device-code }
  else             { openclaw models auth login --provider openai }
}

# 6. Definir modelo padrao na rota canonica openai/*
Step "Definindo modelo padrao: $Model"
$list = openclaw models list --provider openai | Out-String
Write-Host $list
if ($list -match [regex]::Escape($Model.Replace("openai/",""))) {
  openclaw config set agents.defaults.model.primary $Model
} else {
  Write-Warning "$Model nao aparece na sua conta. Rode de novo com -Model <um da lista acima>."
}

# 7. Verificacao
Step "Verificando"
openclaw models status --probe --probe-provider openai
openclaw gateway restart 2>$null

Write-Host "`nPronto. No chat do OpenClaw envie: /codex status  e  /status (deve mostrar 'Runtime: OpenAI Codex')." -ForegroundColor Green
