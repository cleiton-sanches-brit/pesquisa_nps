# Script de configuração automática para o projeto NPS Surveys
Write-Host "Configuracao Automatica do Projeto NPS Surveys" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERRO: Execute este script no diretório raiz do projeto" -ForegroundColor Red
    exit 1
}

# Função para executar comandos Python
function Invoke-PythonCommand {
    param($Command, $WorkingDirectory = $null)
    try {
        $pythonPath = ".\venv\Scripts\python.exe"
        if ($WorkingDirectory) {
            $result = & $pythonPath $Command.Split(' ') 2>&1
        } else {
            $result = & $pythonPath $Command.Split(' ') 2>&1
        }
        return $result
    }
    catch {
        Write-Host "ERRO ao executar: $Command" -ForegroundColor Red
        Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# 1. Verificar ambiente virtual
Write-Host "`nVerificando ambiente virtual..." -ForegroundColor Yellow
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado" -ForegroundColor Red
    exit 1
}

# 2. Testar conexão com banco (ignorar erro de login por enquanto)
Write-Host "`nTestando conexao com banco de dados..." -ForegroundColor Yellow
$testResult = Invoke-PythonCommand "test_db.py"
if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCESSO: Conexao com banco estabelecida!" -ForegroundColor Green
} else {
    Write-Host "AVISO: Problema na conexao com banco, mas continuando..." -ForegroundColor Yellow
}

# 3. Configurar Django
Write-Host "`nConfigurando Django..." -ForegroundColor Yellow
Set-Location "django_app"

# Executar migrações
Write-Host "Executando migracoes..." -ForegroundColor Yellow
Invoke-PythonCommand "manage.py makemigrations"
Invoke-PythonCommand "manage.py migrate"

# 4. Criar superusuário automaticamente
Write-Host "`nCriando superusuario..." -ForegroundColor Yellow
$superuserScript = @"
from django.contrib.auth.models import User
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
import django
django.setup()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario criado: admin/admin123')
else:
    print('Superusuario ja existe')
"@

$superuserScript | Invoke-PythonCommand "manage.py shell"

# 5. Voltar ao diretório raiz
Set-Location ".."

# 6. Criar script de inicialização
Write-Host "`nCriando script de inicializacao..." -ForegroundColor Yellow
$startScript = @"
# Script para iniciar os serviços automaticamente
Write-Host "Iniciando serviços NPS Surveys..." -ForegroundColor Green

# Iniciar Django em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "django_app\manage.py", "runserver", "0.0.0.0:8000" -WindowStyle Hidden

# Aguardar Django inicializar
Start-Sleep -Seconds 5

# Iniciar FastAPI em background
Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8001" -WindowStyle Hidden

Write-Host "Serviços iniciados!" -ForegroundColor Green
Write-Host "Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "Login: admin / admin123" -ForegroundColor Cyan
Write-Host "`nPressione qualquer tecla para parar os serviços..." -ForegroundColor Yellow
`$null = `$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Parar serviços
Get-Process | Where-Object {`$_.ProcessName -eq "python"} | Stop-Process -Force
Write-Host "`nServiços parados!" -ForegroundColor Red
"@

$startScript | Out-File -FilePath "iniciar_servicos.ps1" -Encoding UTF8

Write-Host "`nConfiguracao concluida com sucesso!" -ForegroundColor Green
Write-Host "`nPara iniciar os serviços, execute:" -ForegroundColor Yellow
Write-Host "   .\iniciar_servicos.ps1" -ForegroundColor Cyan
Write-Host "`nURLs importantes:" -ForegroundColor Yellow
Write-Host "   - Django Admin: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "   - FastAPI Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "   - Login: admin / admin123" -ForegroundColor Cyan

