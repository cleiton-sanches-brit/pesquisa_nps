# Script para fazer commit e push para GitHub
# Repositório: https://github.com/cleiton-sanches-brit/pesquisa_nps

Write-Host "🔗 Configurando repositório GitHub...`n" -ForegroundColor Cyan

# Navegar para o diretório do projeto
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectPath = Join-Path $scriptPath "pesquisas_nps"
Set-Location $projectPath

# Verificar Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não encontrado! Reinicie o terminal após instalar." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Inicializar Git se necessário
if (-not (Test-Path ".git")) {
    Write-Host "📦 Inicializando repositório Git..." -ForegroundColor Yellow
    git init | Out-Null
    Write-Host "✅ Repositório inicializado" -ForegroundColor Green
}

# Configurar remote
Write-Host "🔗 Configurando remote origin..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/cleiton-sanches-brit/pesquisa_nps.git
Write-Host "✅ Remote configurado" -ForegroundColor Green

# Configurar Git se necessário
$userName = git config user.name 2>$null
$userEmail = git config user.email 2>$null
if (-not $userName -or -not $userEmail) {
    Write-Host "`n⚙️  Configurando Git (primeira vez)..." -ForegroundColor Yellow
    git config --global user.name "Cleiton Sanches"
    git config --global user.email "cleiton.sanches@exemplo.com"
    Write-Host "✅ Git configurado" -ForegroundColor Green
}

Write-Host ""

# Adicionar arquivos
Write-Host "📝 Adicionando arquivos..." -ForegroundColor Yellow
git add .
Write-Host "✅ Arquivos adicionados" -ForegroundColor Green

# Fazer commit
Write-Host "`n💾 Fazendo commit..." -ForegroundColor Yellow
git commit -m "Commit inicial - Sistema de Pesquisas NPS"
Write-Host "✅ Commit realizado" -ForegroundColor Green

# Renomear branch
Write-Host "`n🌿 Configurando branch main..." -ForegroundColor Yellow
git branch -M main

# Push para GitHub
Write-Host "`n📤 Enviando para GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANTE: GitHub não aceita mais senha normal!" -ForegroundColor Red
Write-Host "Você precisa usar um Personal Access Token.`n" -ForegroundColor Yellow
Write-Host "Se ainda não tem um token:" -ForegroundColor White
Write-Host "1. Acesse: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host "2. Clique em 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Marque a opção 'repo' (acesso completo)" -ForegroundColor White
Write-Host "4. Copie o token gerado`n" -ForegroundColor White
Write-Host "Quando pedir senha, cole o TOKEN (não sua senha)`n" -ForegroundColor Yellow

Read-Host "Pressione Enter para continuar com o push..."

try {
    git push -u origin main
    Write-Host ""
    Write-Host "✅ Código enviado para GitHub com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Repositório: https://github.com/cleiton-sanches-brit/pesquisa_nps" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- Token inválido ou expirado" -ForegroundColor White
    Write-Host "- Repositório não existe ou sem permissão" -ForegroundColor White
    Write-Host "- Problema de conexão" -ForegroundColor White
    Write-Host ""
    Write-Host "Tente novamente com um token válido." -ForegroundColor Yellow
}

Write-Host ""

