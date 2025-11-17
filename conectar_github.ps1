# Script para conectar projeto ao GitHub
# Uso: .\conectar_github.ps1

Write-Host "🔗 Conectar Projeto ao GitHub`n" -ForegroundColor Cyan

# Verificar Git
try {
    git --version | Out-Null
} catch {
    Write-Host "❌ Git não está instalado! Instale em: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# Navegar para o diretório do projeto
if ($PSScriptRoot) {
    $projectPath = Join-Path (Split-Path -Parent $PSScriptRoot) "pesquisas_nps"
} else {
    $projectPath = Join-Path $PWD "pesquisas_nps"
}
if (Test-Path $projectPath) {
    Set-Location $projectPath
} else {
    # Se não encontrar, usar diretório atual
    Write-Host "⚠️  Usando diretório atual: $PWD" -ForegroundColor Yellow
}

# Inicializar Git se necessário
if (-not (Test-Path ".git")) {
    git init | Out-Null
}

# Verificar e remover remote existente se necessário
$remotes = git remote -v 2>$null
if ($remotes) {
    Write-Host "Remote existente encontrado:`n$remotes`n" -ForegroundColor Yellow
    $changeRemote = Read-Host "Deseja alterar? (s/n)"
    if ($changeRemote -eq "s" -or $changeRemote -eq "S") {
        git remote remove origin 2>$null
    } else {
        exit 0
    }
}

# Solicitar informações
Write-Host "`n📝 Informações do Repositório GitHub" -ForegroundColor Cyan
$githubUser = Read-Host "Usuário do GitHub"
$repoName = Read-Host "Nome do repositório"
$connectionType = Read-Host "Tipo de conexão (1=HTTPS, 2=SSH) [1]"

$remoteUrl = if ($connectionType -eq "2") {
    "git@github.com:$githubUser/$repoName.git"
} else {
    "https://github.com/$githubUser/$repoName.git"
}

# Adicionar remote
git remote add origin $remoteUrl
Write-Host "✅ Remote adicionado: $remoteUrl`n" -ForegroundColor Green

# Configurar Git se necessário
$userName = git config user.name
$userEmail = git config user.email
if (-not $userName -or -not $userEmail) {
    $configName = Read-Host "Nome (para commits)"
    $configEmail = Read-Host "Email (para commits)"
    git config --global user.name $configName
    git config --global user.email $configEmail
}

# Commit e push opcional
$doCommit = Read-Host "`nFazer commit e push agora? (s/n)"
if ($doCommit -eq "s" -or $doCommit -eq "S") {
    git add .
    $commitMessage = Read-Host "Mensagem do commit [Enter para padrão]"
    if (-not $commitMessage) {
        $commitMessage = "Commit inicial - Sistema de Pesquisas NPS"
    }
    git commit -m $commitMessage
    
    $branchName = Read-Host "Nome da branch [main]"
    if (-not $branchName) { $branchName = "main" }
    git branch -M $branchName
    
    Write-Host "`n⚠️  Use Personal Access Token como senha: https://github.com/settings/tokens`n" -ForegroundColor Yellow
    git push -u origin $branchName
    
    Write-Host "`n✅ Repositório: https://github.com/$githubUser/$repoName" -ForegroundColor Green
} else {
    Write-Host "`nℹ️  Execute manualmente:" -ForegroundColor Yellow
    Write-Host "   git add ." -ForegroundColor White
    Write-Host "   git commit -m 'msg'" -ForegroundColor White
    Write-Host "   git push -u origin main" -ForegroundColor White
}

Write-Host "`n✅ Concluído!" -ForegroundColor Green

