# Script PowerShell para facilitar o deploy no Azure App Service
# Este script ajuda a configurar e fazer deploy da aplicação

param(
    [string]$AppServiceName = "",
    [string]$ResourceGroup = "",
    [string]$SubscriptionId = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deploy para Azure App Service" -ForegroundColor Cyan
Write-Host "  Sistema de Pesquisas NPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Azure CLI está instalado
$azCli = Get-Command az -ErrorAction SilentlyContinue
if (-not $azCli) {
    Write-Host "ERRO: Azure CLI não está instalado!" -ForegroundColor Red
    Write-Host "Instale em: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Azure CLI encontrado" -ForegroundColor Green

# Verificar se está logado no Azure
Write-Host "Verificando login no Azure..." -ForegroundColor Yellow
$account = az account show 2>$null | ConvertFrom-Json
if (-not $account) {
    Write-Host "Fazendo login no Azure..." -ForegroundColor Yellow
    az login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: Falha ao fazer login no Azure" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Logado no Azure" -ForegroundColor Green
Write-Host "  Conta: $($account.user.name)" -ForegroundColor Gray
Write-Host "  Subscription: $($account.name)" -ForegroundColor Gray
Write-Host ""

# Solicitar informações se não foram fornecidas
if ([string]::IsNullOrEmpty($AppServiceName)) {
    $AppServiceName = Read-Host "Nome do App Service"
}

if ([string]::IsNullOrEmpty($ResourceGroup)) {
    $ResourceGroup = Read-Host "Nome do Resource Group"
}

# Verificar se o App Service existe
Write-Host "Verificando App Service '$AppServiceName'..." -ForegroundColor Yellow
$appService = az webapp show --name $AppServiceName --resource-group $ResourceGroup 2>$null | ConvertFrom-Json

if (-not $appService) {
    Write-Host "ERRO: App Service '$AppServiceName' não encontrado no Resource Group '$ResourceGroup'" -ForegroundColor Red
    Write-Host ""
    Write-Host "Deseja criar o App Service? (S/N)" -ForegroundColor Yellow
    $create = Read-Host
    if ($create -eq "S" -or $create -eq "s") {
        Write-Host "Criando App Service..." -ForegroundColor Yellow
        # Aqui você pode adicionar comandos para criar o App Service
        Write-Host "Use o Azure Portal ou execute:" -ForegroundColor Yellow
        Write-Host "az webapp create --name $AppServiceName --resource-group $ResourceGroup --runtime 'PYTHON:3.12' --plan [nome-do-plano]" -ForegroundColor Gray
        exit 0
    } else {
        exit 1
    }
}

Write-Host "✓ App Service encontrado" -ForegroundColor Green
Write-Host "  URL: https://$($appService.defaultHostName)" -ForegroundColor Gray
Write-Host ""

# Configurar startup command
Write-Host "Configurando startup command..." -ForegroundColor Yellow
az webapp config set --name $AppServiceName --resource-group $ResourceGroup --startup-file "startup.sh"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Startup command configurado" -ForegroundColor Green
} else {
    Write-Host "⚠ Aviso: Falha ao configurar startup command" -ForegroundColor Yellow
}

# Configurar working directory
Write-Host "Configurando working directory..." -ForegroundColor Yellow
az webapp config appsettings set --name $AppServiceName --resource-group $ResourceGroup --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true ENABLE_ORYX_BUILD=true
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Configurações de build atualizadas" -ForegroundColor Green
} else {
    Write-Host "⚠ Aviso: Falha ao configurar build settings" -ForegroundColor Yellow
}

# Verificar variáveis de ambiente
Write-Host ""
Write-Host "Verificando variáveis de ambiente..." -ForegroundColor Yellow
$settings = az webapp config appsettings list --name $AppServiceName --resource-group $ResourceGroup | ConvertFrom-Json

$requiredVars = @("SECRET_KEY", "DEBUG", "ALLOWED_HOSTS", "DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "SENDGRID_API_KEY")
$missingVars = @()

foreach ($var in $requiredVars) {
    $found = $settings | Where-Object { $_.name -eq $var }
    if (-not $found) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "⚠ Variáveis de ambiente faltando:" -ForegroundColor Yellow
    foreach ($var in $missingVars) {
        Write-Host "  - $var" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Configure essas variáveis no Azure Portal:" -ForegroundColor Yellow
    Write-Host "  App Service → Configuration → Application settings" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "✓ Todas as variáveis obrigatórias estão configuradas" -ForegroundColor Green
}

# Verificar deployment
Write-Host ""
Write-Host "Verificando configuração de deployment..." -ForegroundColor Yellow
$deployment = az webapp deployment source show --name $AppServiceName --resource-group $ResourceGroup 2>$null | ConvertFrom-Json

if ($deployment) {
    Write-Host "✓ Deployment configurado" -ForegroundColor Green
    Write-Host "  Repositório: $($deployment.repoUrl)" -ForegroundColor Gray
    Write-Host "  Branch: $($deployment.branch)" -ForegroundColor Gray
} else {
    Write-Host "⚠ Deployment não configurado" -ForegroundColor Yellow
    Write-Host "Configure no Azure Portal: Deployment Center" -ForegroundColor Gray
}

# Resumo
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resumo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "App Service: $AppServiceName" -ForegroundColor White
Write-Host "Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host "URL: https://$($appService.defaultHostName)" -ForegroundColor White
Write-Host ""

if ($missingVars.Count -gt 0) {
    Write-Host "⚠ AÇÃO NECESSÁRIA: Configure as variáveis de ambiente faltando" -ForegroundColor Yellow
} else {
    Write-Host "✓ Pronto para deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para fazer deploy:" -ForegroundColor Yellow
    Write-Host "1. Faça commit e push das mudanças para o GitHub" -ForegroundColor Gray
    Write-Host "2. O Azure fará deploy automaticamente (se configurado)" -ForegroundColor Gray
    Write-Host "3. Ou execute: az webapp up --name $AppServiceName --resource-group $ResourceGroup" -ForegroundColor Gray
}

Write-Host ""



