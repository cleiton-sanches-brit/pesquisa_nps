# Script corrigido para iniciar os serviços
Write-Host "Iniciando serviços NPS Surveys..." -ForegroundColor Green

# Parar processos Python existentes
Write-Host "Parando processos Python existentes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Usar o caminho completo do Python
$pythonPath = "C:\Users\CleitonSanchesBR-iT\AppData\Local\Programs\Python\Python312\python.exe"
$venvPythonPath = ".\venv\Scripts\python.exe"

# Verificar qual Python usar
if (Test-Path $venvPythonPath) {
    $pythonCmd = $venvPythonPath
    Write-Host "Usando Python do ambiente virtual" -ForegroundColor Green
} else {
    $pythonCmd = $pythonPath
    Write-Host "Usando Python do sistema" -ForegroundColor Yellow
}

# Iniciar Django
Write-Host "`nIniciando Django..." -ForegroundColor Yellow
$djangoArgs = @("django_app\manage.py", "runserver", "0.0.0.0:8000")
Start-Process -FilePath $pythonCmd -ArgumentList $djangoArgs -WindowStyle Normal

# Aguardar Django inicializar
Write-Host "Aguardando Django inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Testar Django
Write-Host "`nTestando Django..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 5
    Write-Host "SUCESSO: Django está rodando!" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Django não está respondendo" -ForegroundColor Red
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Iniciar FastAPI
Write-Host "`nIniciando FastAPI..." -ForegroundColor Yellow
$fastapiArgs = @("-m", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001")
Start-Process -FilePath $pythonCmd -ArgumentList $fastapiArgs -WindowStyle Normal

# Aguardar FastAPI inicializar
Write-Host "Aguardando FastAPI inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Testar FastAPI
Write-Host "`nTestando FastAPI..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001" -UseBasicParsing -TimeoutSec 5
    Write-Host "SUCESSO: FastAPI está rodando!" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
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

