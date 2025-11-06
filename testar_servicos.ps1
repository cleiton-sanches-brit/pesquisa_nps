# Script para testar os serviços
Write-Host "Testando serviços NPS Surveys..." -ForegroundColor Green

# Testar Django
Write-Host "`nTestando Django..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 10
    Write-Host "SUCESSO: Django está rodando na porta 8000" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Django não está rodando na porta 8000" -ForegroundColor Red
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Testar FastAPI
Write-Host "`nTestando FastAPI..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001" -UseBasicParsing -TimeoutSec 10
    Write-Host "SUCESSO: FastAPI está rodando na porta 8001" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "ERRO: FastAPI não está rodando na porta 8001" -ForegroundColor Red
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar processos Python
Write-Host "`nVerificando processos Python..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Processos Python encontrados: $($pythonProcesses.Count)" -ForegroundColor Green
    foreach ($process in $pythonProcesses) {
        Write-Host "  PID: $($process.Id) - $($process.ProcessName)" -ForegroundColor Cyan
    }
} else {
    Write-Host "Nenhum processo Python encontrado" -ForegroundColor Red
}

Write-Host "`nTeste concluído!" -ForegroundColor Green

