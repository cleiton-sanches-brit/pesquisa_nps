# Script simples para iniciar o servidor Django
Write-Host "Iniciando servidor Django..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "django_app")) {
    Write-Host "ERRO: Execute este script no diretório raiz do projeto" -ForegroundColor Red
    exit 1
}

# Verificar ambiente virtual
$venvPython = ".\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nMudando para diretorio django_app..." -ForegroundColor Yellow
Set-Location "django_app"

Write-Host "`nIniciando servidor Django na porta 8000..." -ForegroundColor Yellow
Write-Host "Acesse: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "`nPressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""

# Iniciar servidor
& "..\venv\Scripts\python.exe" manage.py runserver
