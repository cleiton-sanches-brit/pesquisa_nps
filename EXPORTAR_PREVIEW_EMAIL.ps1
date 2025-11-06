# Script PowerShell para exportar preview de email
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Exportando Preview de Email para PDF/PNG" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "pesquisas_nps"
..\venv\Scripts\python.exe exportar_preview_email.py

Write-Host ""
Write-Host "Exportacao concluida!" -ForegroundColor Green
Write-Host "Verifique a pasta 'exports' para os arquivos gerados." -ForegroundColor Yellow
Write-Host ""

# Abrir pasta de exports
$exportsPath = Join-Path (Get-Location) "exports"
if (Test-Path $exportsPath) {
    Write-Host "Abrindo pasta de exports..." -ForegroundColor Cyan
    Start-Process explorer.exe -ArgumentList $exportsPath
}

