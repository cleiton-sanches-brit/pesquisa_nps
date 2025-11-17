# Script para testar os templates
Write-Host "Guia de Teste dos Templates" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "`nDados de teste criados com sucesso!" -ForegroundColor Cyan
Write-Host "`nURLs para testar:" -ForegroundColor Yellow
Write-Host "  1. Lista de convites: http://localhost:8000/survey/1/invitations/" -ForegroundColor White
Write-Host "  2. Enviar convites: http://localhost:8000/survey/1/invite/" -ForegroundColor White
Write-Host "  3. Responder pesquisa: http://localhost:8000/survey/1/respond/7ff55155-1afa-45ba-bc2a-0848a1963e68/" -ForegroundColor White

Write-Host "`nVerificando se o servidor Django esta rodando..." -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    Write-Host "OK: Servidor Django esta rodando!" -ForegroundColor Green
    Write-Host "`nAcesse as URLs acima no navegador para testar os templates." -ForegroundColor Cyan
} catch {
    Write-Host "AVISO: Servidor Django nao esta rodando!" -ForegroundColor Yellow
    Write-Host "`nPara iniciar o servidor:" -ForegroundColor Yellow
    Write-Host "  1. Execute: .\iniciar_corrigido.ps1" -ForegroundColor Cyan
    Write-Host "  2. Ou manualmente:" -ForegroundColor Cyan
    Write-Host "     cd django_app" -ForegroundColor White
    Write-Host "     ..\venv\Scripts\python.exe manage.py runserver" -ForegroundColor White
}

Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "Consulte GUIA_TESTE_TEMPLATES.md para mais detalhes" -ForegroundColor Cyan
