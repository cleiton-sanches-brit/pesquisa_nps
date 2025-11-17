# Script para iniciar os serviços manualmente
Write-Host "Iniciando serviços NPS Surveys..." -ForegroundColor Green

# Parar processos Python existentes
Write-Host "Parando processos Python existentes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Iniciar Django
Write-Host "`nIniciando Django..." -ForegroundColor Yellow
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "django_app\manage.py", "runserver", "0.0.0.0:8000" -WindowStyle Normal

# Aguardar Django inicializar
Write-Host "Aguardando Django inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Testar Django
Write-Host "`nTestando Django..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 5
    Write-Host "SUCESSO: Django está rodando!" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Django não está respondendo" -ForegroundColor Red
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Iniciar FastAPI
Write-Host "`nIniciando FastAPI..." -ForegroundColor Yellow
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001" -WindowStyle Normal

# Aguardar FastAPI inicializar
Write-Host "Aguardando FastAPI inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Testar FastAPI
Write-Host "`nTestando FastAPI..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001" -UseBasicParsing -TimeoutSec 5
    Write-Host "SUCESSO: FastAPI está rodando!" -ForegroundColor Green
} catch {
    Write-Host "ERRO: FastAPI não está respondendo" -ForegroundColor Red
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nServiços iniciados!" -ForegroundColor Green
Write-Host "Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "Login: admin / admin123" -ForegroundColor Cyan

Write-Host "`nPressione qualquer tecla para parar os serviços..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Parar serviços
Write-Host "`nParando serviços..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "Serviços parados!" -ForegroundColor Red

