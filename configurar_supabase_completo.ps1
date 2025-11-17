# Script para configurar projeto com Supabase PostgreSQL
Write-Host "Configuracao do Projeto NPS Surveys com Supabase" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Credenciais do Supabase
$supabaseHost = "aws-1-us-east-2.pooler.supabase.com"
$supabasePort = "6543"
$supabaseDatabase = "postgres"
$supabaseUser = "postgres.pzumhkxjasqntwujdztg"
$supabasePassword = "Pds2025@@"

Write-Host "`nConfigurando credenciais do Supabase..." -ForegroundColor Yellow
Write-Host "Host: $supabaseHost" -ForegroundColor Cyan
Write-Host "Porta: $supabasePort" -ForegroundColor Cyan
Write-Host "Database: $supabaseDatabase" -ForegroundColor Cyan
Write-Host "User: $supabaseUser" -ForegroundColor Cyan

# Atualizar arquivo .env
Write-Host "`nAtualizando arquivo .env..." -ForegroundColor Yellow

$envContent = @"
# Django Settings
SECRET_KEY=+yrkvd)9n%+g&7zc6v)%_-+yr%b)cu@7a1-5n*x()she+!2m9q
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase PostgreSQL Settings
DB_ENGINE=postgresql
DB_HOST=$supabaseHost
DB_PORT=$supabasePort
DB_NAME=$supabaseDatabase
DB_USER=$supabaseUser
DB_PASSWORD=$supabasePassword

# API Settings
DJANGO_API_URL=http://localhost:8000
FASTAPI_URL=http://localhost:8001
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8 -Force
Write-Host "Arquivo .env atualizado!" -ForegroundColor Green

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

$settingsContent = @"
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-temporary-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'surveys',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nps_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nps_admin.wsgi.application'

# Database - Supabase PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 600,  # 10 minutos
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
"@

$settingsContent | Out-File -FilePath "django_app\nps_admin\settings.py" -Encoding UTF8 -Force
Write-Host "settings.py atualizado para usar Supabase!" -ForegroundColor Green

# Testar conexão
Write-Host "`nTestando conexao com Supabase..." -ForegroundColor Yellow
$testResult = & $pythonPath "database\test_supabase_connection.py"
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nConexao testada com sucesso!" -ForegroundColor Green
} else {
    Write-Host "`nAVISO: Teste de conexao falhou. Verifique:" -ForegroundColor Yellow
    Write-Host "  1. Se o script SQL foi executado no Supabase SQL Editor" -ForegroundColor Cyan
    Write-Host "  2. Se as credenciais estao corretas" -ForegroundColor Cyan
    Write-Host "  3. Se o firewall permite conexoes" -ForegroundColor Cyan
    Write-Host "`nContinando mesmo assim para executar migracoes..." -ForegroundColor Yellow
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
Write-Host "  1. Execute o script SQL no Supabase SQL Editor (database/supabase_schema.sql)" -ForegroundColor Cyan
Write-Host "  2. Crie um superusuario: python django_app\manage.py createsuperuser" -ForegroundColor Cyan
Write-Host "  3. Inicie o servidor: python django_app\manage.py runserver" -ForegroundColor Cyan
Write-Host "`nAcesse: http://localhost:8000/admin/" -ForegroundColor Green
