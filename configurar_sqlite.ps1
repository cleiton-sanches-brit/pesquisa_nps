# Script de configuração automática usando SQLite temporariamente
Write-Host "Configuracao Automatica do Projeto NPS Surveys (SQLite)" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

# Verificar se estamos no diretório correto
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERRO: Execute este script no diretório raiz do projeto" -ForegroundColor Red
    exit 1
}

# 1. Configurar Django para usar SQLite temporariamente
Write-Host "`nConfigurando Django para usar SQLite..." -ForegroundColor Yellow

# Backup do settings original
Copy-Item "django_app\nps_admin\settings.py" "django_app\nps_admin\settings_backup.py"

# Criar settings temporário com SQLite
$sqliteSettings = @"
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

# Database - SQLite temporário
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
"@

$sqliteSettings | Out-File -FilePath "django_app\nps_admin\settings.py" -Encoding UTF8

# 2. Executar migrações
Write-Host "`nExecutando migracoes..." -ForegroundColor Yellow
Set-Location "django_app"

& "..\venv\Scripts\python.exe" manage.py makemigrations
& "..\venv\Scripts\python.exe" manage.py migrate

# 3. Criar superusuário
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

$superuserScript | & "..\venv\Scripts\python.exe" manage.py shell

# 4. Voltar ao diretório raiz
Set-Location ".."

# 5. Criar script de inicialização
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
Write-Host "`nNOTA: Usando SQLite temporariamente. Para usar SQL Server," -ForegroundColor Yellow
Write-Host "      configure as credenciais corretas e restaure o settings original." -ForegroundColor Yellow

