# Script para configurar projeto com Supabase PostgreSQL
Write-Host "Configuracao do Projeto NPS Surveys com Supabase" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "`nAVISO: Arquivo .env nao encontrado!" -ForegroundColor Yellow
    Write-Host "Criando arquivo .env a partir do template..." -ForegroundColor Yellow
    
    if (Test-Path ".env.supabase.template") {
        Copy-Item ".env.supabase.template" ".env"
        Write-Host "Arquivo .env criado. Por favor, edite com suas credenciais do Supabase." -ForegroundColor Cyan
        Write-Host "Pressione qualquer tecla apos editar o .env..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } else {
        Write-Host "ERRO: Template .env.supabase.template nao encontrado!" -ForegroundColor Red
        exit 1
    }
}

# Carregar variáveis do .env
$envContent = Get-Content ".env" | Where-Object { $_ -match '^[^#].*=' }
$envVars = @{}
foreach ($line in $envContent) {
    if ($line -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Verificar credenciais do Supabase
Write-Host "`nVerificando credenciais do Supabase..." -ForegroundColor Yellow

$dbHost = $envVars['DB_HOST']
$dbPassword = $envVars['DB_PASSWORD']

if (-not $dbHost -or $dbHost -eq 'db.xxxxxxxxxxxxx.supabase.co' -or 
    -not $dbPassword -or $dbPassword -eq 'SUA_SENHA_AQUI') {
    Write-Host "`nERRO: Credenciais do Supabase nao configuradas!" -ForegroundColor Red
    Write-Host "`nPor favor, edite o arquivo .env com suas credenciais:" -ForegroundColor Yellow
    Write-Host "  1. DB_HOST=db.xxxxxxxxxxxxx.supabase.co" -ForegroundColor Cyan
    Write-Host "  2. DB_PASSWORD=sua_senha_aqui" -ForegroundColor Cyan
    Write-Host "`nExecute este script novamente apos configurar." -ForegroundColor Yellow
    exit 1
}

Write-Host "Credenciais encontradas!" -ForegroundColor Green

# Verificar se psycopg2 está instalado
Write-Host "`nVerificando driver PostgreSQL (psycopg2)..." -ForegroundColor Yellow

$pythonPath = ".\venv\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

$psycopg2Check = & $pythonPath -c "import psycopg2; print('OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "psycopg2 nao instalado. Instalando..." -ForegroundColor Yellow
    & $pythonPath -m pip install psycopg2-binary
    if ($LASTEXITCODE -eq 0) {
        Write-Host "psycopg2 instalado com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "ERRO ao instalar psycopg2!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "psycopg2 ja esta instalado!" -ForegroundColor Green
}

# Atualizar settings.py para usar Supabase
Write-Host "`nConfigurando settings.py para Supabase..." -ForegroundColor Yellow

if (Test-Path "django_app\nps_admin\settings_supabase.py") {
    $supabaseSettings = Get-Content "django_app\nps_admin\settings_supabase.py" -Raw
    
    # Substituir settings.py
    $supabaseSettings | Out-File -FilePath "django_app\nps_admin\settings.py" -Encoding UTF8
    Write-Host "settings.py atualizado para usar Supabase!" -ForegroundColor Green
} else {
    Write-Host "AVISO: settings_supabase.py nao encontrado. Verifique manualmente." -ForegroundColor Yellow
}

# Testar conexão
Write-Host "`nTestando conexao com Supabase..." -ForegroundColor Yellow
$testResult = & $pythonPath "database\test_supabase_connection.py"
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nConexao testada com sucesso!" -ForegroundColor Green
} else {
    Write-Host "`nAVISO: Teste de conexao falhou. Verifique:" -ForegroundColor Yellow
    Write-Host "  1. Se o script SQL foi executado no Supabase" -ForegroundColor Cyan
    Write-Host "  2. Se as credenciais estao corretas" -ForegroundColor Cyan
    Write-Host "  3. Se o firewall permite conexoes" -ForegroundColor Cyan
}

# Executar migrações
Write-Host "`nExecutando migracoes do Django..." -ForegroundColor Yellow
Set-Location "django_app"
& "..\venv\Scripts\python.exe" manage.py makemigrations
& "..\venv\Scripts\python.exe" manage.py migrate --run-syncdb
Set-Location ".."

Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "Configuracao concluida!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "`nProximos passos:" -ForegroundColor Yellow
Write-Host "  1. Execute o script SQL no Supabase SQL Editor (se ainda nao fez)" -ForegroundColor Cyan
Write-Host "  2. Crie um superusuario: python django_app\manage.py createsuperuser" -ForegroundColor Cyan
Write-Host "  3. Inicie o servidor: python django_app\manage.py runserver" -ForegroundColor Cyan
