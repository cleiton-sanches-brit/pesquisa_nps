# Script para iniciar os serviÃ§os automaticamente
Write-Host "Iniciando serviÃ§os NPS Surveys..." -ForegroundColor Green

# Iniciar Django em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "django_app\manage.py", "runserver", "0.0.0.0:8000" -WindowStyle Hidden

# Aguardar Django inicializar
Start-Sleep -Seconds 5

# Iniciar FastAPI em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001" -WindowStyle Hidden

Write-Host "ServiÃ§os iniciados!" -ForegroundColor Green
Write-Host "Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "Login: admin / admin123" -ForegroundColor Cyan
Write-Host "
Pressione qualquer tecla para parar os serviÃ§os..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Parar serviÃ§os
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Write-Host "
ServiÃ§os parados!" -ForegroundColor Red
