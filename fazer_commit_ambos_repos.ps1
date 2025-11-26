# Script para fazer commit e push para ambos os repositórios GitHub
# cleiton-sanches-brit/pesquisa_nps e britsoftware/PesquisaNPS

param(
    [string]$MensagemCommit = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Commit e Push para Ambos Repositórios" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path ".git")) {
    Write-Host "ERRO: Não é um repositório Git!" -ForegroundColor Red
    Write-Host "Execute este script dentro da pasta pesquisas_nps" -ForegroundColor Yellow
    exit 1
}

# Verificar remotes configurados
Write-Host "Verificando repositórios remotos..." -ForegroundColor Yellow
$remotes = git remote -v

if ($remotes -notmatch "origin") {
    Write-Host "ERRO: Remote 'origin' não encontrado!" -ForegroundColor Red
    exit 1
}

if ($remotes -notmatch "britsoftware") {
    Write-Host "ERRO: Remote 'britsoftware' não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Repositórios remotos encontrados:" -ForegroundColor Green
Write-Host "  - origin (cleiton-sanches-brit/pesquisa_nps)" -ForegroundColor Gray
Write-Host "  - britsoftware (britsoftware/PesquisaNPS)" -ForegroundColor Gray
Write-Host ""

# Verificar status do Git
Write-Host "Verificando status do repositório..." -ForegroundColor Yellow
$status = git status --porcelain

if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "⚠ Nenhuma alteração para commitar!" -ForegroundColor Yellow
    Write-Host "Deseja fazer push mesmo assim? (S/N)" -ForegroundColor Yellow
    $continuar = Read-Host
    if ($continuar -ne "S" -and $continuar -ne "s") {
        exit 0
    }
} else {
    Write-Host "Alterações encontradas:" -ForegroundColor Green
    git status --short
    Write-Host ""
}

# Solicitar mensagem de commit se não foi fornecida
if ([string]::IsNullOrWhiteSpace($MensagemCommit)) {
    Write-Host "Digite a mensagem do commit:" -ForegroundColor Yellow
    $MensagemCommit = Read-Host
    if ([string]::IsNullOrWhiteSpace($MensagemCommit)) {
        Write-Host "ERRO: Mensagem de commit é obrigatória!" -ForegroundColor Red
        exit 1
    }
}

# Adicionar todos os arquivos
Write-Host ""
Write-Host "Adicionando arquivos ao staging..." -ForegroundColor Yellow
git add .

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao adicionar arquivos!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Arquivos adicionados" -ForegroundColor Green

# Fazer commit
Write-Host ""
Write-Host "Fazendo commit..." -ForegroundColor Yellow
git commit -m $MensagemCommit

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao fazer commit!" -ForegroundColor Red
    Write-Host "Verifique se há alterações para commitar." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Commit realizado com sucesso" -ForegroundColor Green
Write-Host ""

# Push para origin (cleiton-sanches-brit/pesquisa_nps)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Push para origin (cleiton-sanches-brit)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Fazendo push para origin/main..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Push para origin realizado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "⚠ ERRO ao fazer push para origin!" -ForegroundColor Red
    Write-Host "Continuando com o próximo repositório..." -ForegroundColor Yellow
}

Write-Host ""

# Push para britsoftware (britsoftware/PesquisaNPS)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Push para britsoftware (britsoftware)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Fazendo push para britsoftware/main..." -ForegroundColor Yellow
git push britsoftware main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Push para britsoftware realizado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "⚠ ERRO ao fazer push para britsoftware!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "  - Falta de permissão no repositório britsoftware" -ForegroundColor Gray
    Write-Host "  - Token de acesso expirado ou inválido" -ForegroundColor Gray
    Write-Host "  - Branch 'main' não existe no repositório remoto" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resumo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar último commit
$ultimoCommit = git log -1 --oneline
Write-Host "Último commit: $ultimoCommit" -ForegroundColor White
Write-Host ""

Write-Host "Repositórios:" -ForegroundColor White
Write-Host "  ✓ origin → cleiton-sanches-brit/pesquisa_nps" -ForegroundColor Gray
Write-Host "  ✓ britsoftware → britsoftware/PesquisaNPS" -ForegroundColor Gray
Write-Host ""

Write-Host "Para verificar os repositórios:" -ForegroundColor Yellow
Write-Host "  https://github.com/cleiton-sanches-brit/pesquisa_nps" -ForegroundColor Gray
Write-Host "  https://github.com/britsoftware/PesquisaNPS" -ForegroundColor Gray
Write-Host ""


