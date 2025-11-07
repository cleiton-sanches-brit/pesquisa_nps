# Script para configurar email Microsoft/Office 365
# Email: csanches@br-itsoftware.com.br

Write-Host "📧 Configurando Email Microsoft/Office 365..." -ForegroundColor Cyan
Write-Host ""

# Verificar se .env existe
$envPath = Join-Path $PSScriptRoot "pesquisas_nps\.env"
if (-not (Test-Path $envPath)) {
    Write-Host "Criando arquivo .env..." -ForegroundColor Yellow
    New-Item -Path $envPath -ItemType File -Force | Out-Null
}

# Ler .env existente (se houver)
$envContent = @{}
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $envContent[$matches[1].Trim()] = $matches[2].Trim()
        }
    }
}

# Configurar credenciais Microsoft
Write-Host "Configurando credenciais Microsoft..." -ForegroundColor Yellow

# Email Microsoft/Office 365
$envContent['EMAIL_HOST'] = 'smtp.office365.com'
$envContent['EMAIL_PORT'] = '587'
$envContent['EMAIL_USE_TLS'] = 'True'
$envContent['EMAIL_HOST_USER'] = 'csanches@br-itsoftware.com.br'
$envContent['EMAIL_HOST_PASSWORD'] = 'PDS2025@@'
$envContent['DEFAULT_FROM_EMAIL'] = 'csanches@br-itsoftware.com.br'

# Manter outras configurações se existirem
if (-not $envContent.ContainsKey('SECRET_KEY')) {
    $envContent['SECRET_KEY'] = 'django-insecure-temporary-key-change-in-production'
}
if (-not $envContent.ContainsKey('DEBUG')) {
    $envContent['DEBUG'] = 'True'
}
if (-not $envContent.ContainsKey('ALLOWED_HOSTS')) {
    $envContent['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
}

# Escrever .env
Write-Host "Salvando configurações no .env..." -ForegroundColor Yellow
$output = @()
$output += "# Django Settings"
$output += "SECRET_KEY=$($envContent['SECRET_KEY'])"
$output += "DEBUG=$($envContent['DEBUG'])"
$output += "ALLOWED_HOSTS=$($envContent['ALLOWED_HOSTS'])"
$output += ""
$output += "# Database Settings (manter existentes se houver)"
if ($envContent.ContainsKey('DB_HOST')) {
    $output += "DB_HOST=$($envContent['DB_HOST'])"
    $output += "DB_PORT=$($envContent['DB_PORT'])"
    $output += "DB_NAME=$($envContent['DB_NAME'])"
    $output += "DB_USER=$($envContent['DB_USER'])"
    $output += "DB_PASSWORD=$($envContent['DB_PASSWORD'])"
}
$output += ""
$output += "# Email Settings - Microsoft/Office 365"
$output += "EMAIL_HOST=$($envContent['EMAIL_HOST'])"
$output += "EMAIL_PORT=$($envContent['EMAIL_PORT'])"
$output += "EMAIL_USE_TLS=$($envContent['EMAIL_USE_TLS'])"
$output += "EMAIL_HOST_USER=$($envContent['EMAIL_HOST_USER'])"
$output += "EMAIL_HOST_PASSWORD=$($envContent['EMAIL_HOST_PASSWORD'])"
$output += "DEFAULT_FROM_EMAIL=$($envContent['DEFAULT_FROM_EMAIL'])"

$output | Out-File -FilePath $envPath -Encoding UTF8 -Force

Write-Host ""
Write-Host "✅ Email configurado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "Configurações:" -ForegroundColor Cyan
Write-Host "  Host: smtp.office365.com" -ForegroundColor White
Write-Host "  Porta: 587" -ForegroundColor White
Write-Host "  TLS: True" -ForegroundColor White
Write-Host "  Usuário: csanches@br-itsoftware.com.br" -ForegroundColor White
Write-Host "  From: csanches@br-itsoftware.com.br" -ForegroundColor White
Write-Host ""
Write-Host "📧 Para testar o envio de email, execute:" -ForegroundColor Yellow
Write-Host "   python testar_envio_email.py" -ForegroundColor Cyan
Write-Host ""

