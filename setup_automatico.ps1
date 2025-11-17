# Script de configuração automática para o projeto NPS Surveys
# Este script configura tudo automaticamente sem interferência manual

Write-Host "🚀 Configuração Automática do Projeto NPS Surveys" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Execute este script no diretório raiz do projeto" -ForegroundColor Red
    exit 1
}

# Função para executar comandos
function Invoke-Command {
    param($Command, $WorkingDirectory = $null)
    try {
        $result = Invoke-Expression $Command
        return $result
    }
    catch {
        Write-Host "❌ Erro ao executar: $Command" -ForegroundColor Red
        Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# 1. Verificar se Python está instalado
Write-Host "`n🔍 Verificando Python..." -ForegroundColor Yellow
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "❌ Python não encontrado. Instalando Python..." -ForegroundColor Red
    
    # Tentar instalar Python via winget
    Write-Host "📦 Instalando Python via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    
    # Aguardar instalação
    Start-Sleep -Seconds 30
    
    # Verificar novamente
    $pythonPath = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonPath) {
        Write-Host "❌ Falha na instalação do Python. Instale manualmente e execute novamente." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Python encontrado: $($pythonPath.Source)" -ForegroundColor Green

# 2. Criar ambiente virtual
Write-Host "`n📦 Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force "venv"
}
python -m venv venv

# 3. Ativar ambiente virtual e instalar dependências
Write-Host "`n📦 Instalando dependências..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
& ".\venv\Scripts\pip.exe" install --upgrade pip
& ".\venv\Scripts\pip.exe" install -r requirements.txt

# 4. Testar conexão com banco
Write-Host "`n🗄️ Testando conexão com banco de dados..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" test_connection_simple.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Conexão com banco estabelecida!" -ForegroundColor Green
} else {
    Write-Host "❌ Falha na conexão com banco. Verifique as credenciais no arquivo .env" -ForegroundColor Red
    exit 1
}

# 5. Executar migrações do Django
Write-Host "`n🔄 Executando migrações do Django..." -ForegroundColor Yellow
Set-Location "django_app"
& "..\venv\Scripts\python.exe" manage.py makemigrations
& "..\venv\Scripts\python.exe" manage.py migrate

# 6. Criar superusuário automaticamente
Write-Host "`n👤 Criando superusuário..." -ForegroundColor Yellow
$superuserScript = @"
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
"@

$superuserScript | & "..\venv\Scripts\python.exe" manage.py shell

# 7. Voltar ao diretório raiz
Set-Location ".."

# 8. Criar script de inicialização
Write-Host "`n📝 Criando script de inicialização..." -ForegroundColor Yellow
$startScript = @"
# Script para iniciar os serviços automaticamente
Write-Host "🚀 Iniciando serviços NPS Surveys..." -ForegroundColor Green

# Iniciar Django em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "django_app\manage.py", "runserver", "0.0.0.0:8000" -WindowStyle Hidden

# Aguardar Django inicializar
Start-Sleep -Seconds 5

# Iniciar FastAPI em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001" -WindowStyle Hidden

Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
Write-Host "🌐 Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "🌐 FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "👤 Login: admin / admin123" -ForegroundColor Cyan
Write-Host "`nPressione qualquer tecla para parar os serviços..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Parar serviços
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process -Force
Write-Host "`n🛑 Serviços parados!" -ForegroundColor Red
"@

$startScript | Out-File -FilePath "iniciar_servicos.ps1" -Encoding UTF8

Write-Host "`n🎉 Configuração concluída com sucesso!" -ForegroundColor Green
Write-Host "`n📋 Para iniciar os serviços, execute:" -ForegroundColor Yellow
Write-Host "   .\iniciar_servicos.ps1" -ForegroundColor Cyan
Write-Host "`n🌐 URLs importantes:" -ForegroundColor Yellow
Write-Host "   - Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "   - FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "   - Login: admin / admin123" -ForegroundColor Cyan

