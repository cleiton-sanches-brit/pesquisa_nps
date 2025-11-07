# Script para fazer push com token
# Execute este script e cole o token quando pedir

$env:Path += ";C:\Program Files\Git\cmd"
Set-Location "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps"

Write-Host "📤 Fazendo push para GitHub...`n" -ForegroundColor Cyan

# Limpar credenciais antigas
git credential reject https://github.com 2>$null

# Configurar remote sem token na URL
git remote set-url origin "https://github.com/cleiton-sanches-brit/pesquisa_nps.git"

Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "Quando pedir autenticação:" -ForegroundColor White
Write-Host "  Username: cleiton-sanches-brit" -ForegroundColor Cyan
Write-Host "  Password: COLE SEU TOKEN AQUI (não sua senha)`n" -ForegroundColor Cyan

# Fazer push (vai pedir credenciais)
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "🔗 Repositório: https://github.com/cleiton-sanches-brit/pesquisa_nps" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Erro no push. Verifique:" -ForegroundColor Red
    Write-Host "  1. Token tem permissão 'repo'?" -ForegroundColor Yellow
    Write-Host "  2. Token está correto e não expirado?" -ForegroundColor Yellow
    Write-Host "  3. Repositório existe no GitHub?" -ForegroundColor Yellow
}

