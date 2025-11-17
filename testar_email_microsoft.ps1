# Script para configurar e testar email Microsoft
Write-Host "📧 Configurando Email Microsoft/Office 365..." -ForegroundColor Cyan
Write-Host ""

# Caminho do projeto
$projectPath = Join-Path $PSScriptRoot "pesquisas_nps"
$envPath = Join-Path $projectPath ".env"

# Criar/atualizar .env
$envContent = @"
# Django Settings
SECRET_KEY=django-insecure-temporary-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (Supabase)
DB_HOST=aws-1-us-east-2.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.pzumhkxjasqntwujdztg
DB_PASSWORD=Pds2025@@

# Email Settings - Microsoft/Office 365
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=csanches@br-itsoftware.com.br
EMAIL_HOST_PASSWORD=PDS2025@@
DEFAULT_FROM_EMAIL=csanches@br-itsoftware.com.br
"@

$envContent | Out-File -FilePath $envPath -Encoding UTF8 -Force

Write-Host "✅ Arquivo .env criado/atualizado!" -ForegroundColor Green
Write-Host ""
Write-Host "Configurações de Email:" -ForegroundColor Cyan
Write-Host "  Host: smtp.office365.com" -ForegroundColor White
Write-Host "  Porta: 587" -ForegroundColor White
Write-Host "  TLS: True" -ForegroundColor White
Write-Host "  Usuário: csanches@br-itsoftware.com.br" -ForegroundColor White
Write-Host "  From: csanches@br-itsoftware.com.br" -ForegroundColor White
Write-Host ""

# Verificar se venv existe
$venvPath = Join-Path $PSScriptRoot "pesquisas_nps\venv\Scripts\python.exe"
if (-not (Test-Path $venvPath)) {
    Write-Host "⚠️  Ambiente virtual não encontrado!" -ForegroundColor Yellow
    Write-Host "   Criando ambiente virtual..." -ForegroundColor Yellow
    Set-Location $projectPath
    python -m venv venv
    & "$venvPath" -m pip install --upgrade pip
    & "$venvPath" -m pip install -r requirements.txt
}

Write-Host ""
Write-Host "🧪 Testando envio de email..." -ForegroundColor Yellow
Write-Host ""

# Solicitar email de teste
$emailTeste = Read-Host "Digite um email para testar o envio (ou Enter para pular)"

if ($emailTeste) {
    Set-Location $projectPath
    & "$venvPath" testar_envio_email.py
} else {
    Write-Host ""
    Write-Host "ℹ️  Para testar depois, execute:" -ForegroundColor Yellow
    Write-Host "   cd pesquisas_nps" -ForegroundColor Cyan
    Write-Host "   .\venv\Scripts\python.exe testar_envio_email.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "✅ Configuração concluída! Email pronto para uso." -ForegroundColor Green
}

