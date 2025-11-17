# Script para corrigir o superusuário do Django
Write-Host "Corrigindo superusuário do Django..." -ForegroundColor Green

# Usar o caminho completo do Python
$pythonPath = "C:\Users\CleitonSanchesBR-iT\AppData\Local\Programs\Python\Python312\python.exe"
$venvPythonPath = ".\venv\Scripts\python.exe"

# Verificar qual Python usar
if (Test-Path $venvPythonPath) {
    $pythonCmd = $venvPythonPath
    Write-Host "Usando Python do ambiente virtual" -ForegroundColor Green
} else {
    $pythonCmd = $pythonPath
    Write-Host "Usando Python do sistema" -ForegroundColor Yellow
}

# Navegar para o diretório do Django
Set-Location "django_app"

# Verificar se o superusuário existe
Write-Host "`nVerificando superusuários existentes..." -ForegroundColor Yellow
$checkScript = @"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
import django
django.setup()

from django.contrib.auth.models import User
users = User.objects.filter(is_superuser=True)
print(f"Superusuários encontrados: {users.count()}")
for user in users:
    print(f"  - {user.username} (email: {user.email})")
"@

$checkScript | & $pythonCmd manage.py shell

# Remover superusuário existente se houver
Write-Host "`nRemovendo superusuários existentes..." -ForegroundColor Yellow
$removeScript = @"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
import django
django.setup()

from django.contrib.auth.models import User
User.objects.filter(is_superuser=True).delete()
print("Superusuários removidos")
"@

$removeScript | & $pythonCmd manage.py shell

# Criar novo superusuário
Write-Host "`nCriando novo superusuário..." -ForegroundColor Yellow
$createScript = @"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
import django
django.setup()

from django.contrib.auth.models import User
user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
print(f"Superusuário criado: {user.username}")
print(f"Email: {user.email}")
print(f"É superusuário: {user.is_superuser}")
print(f"É staff: {user.is_staff}")
"@

$createScript | & $pythonCmd manage.py shell

# Verificar se foi criado corretamente
Write-Host "`nVerificando se foi criado corretamente..." -ForegroundColor Yellow
$verifyScript = @"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
import django
django.setup()

from django.contrib.auth.models import User
try:
    user = User.objects.get(username='admin')
    print(f"SUCESSO: Superusuário encontrado")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"É superusuário: {user.is_superuser}")
    print(f"É staff: {user.is_staff}")
    print(f"Ativo: {user.is_active}")
    
    # Testar autenticação
    if user.check_password('admin123'):
        print("SUCESSO: Senha está correta")
    else:
        print("ERRO: Senha está incorreta")
        
except User.DoesNotExist:
    print("ERRO: Superusuário não encontrado")
"@

$verifyScript | & $pythonCmd manage.py shell

# Voltar ao diretório raiz
Set-Location ".."

Write-Host "`nCorreção concluída!" -ForegroundColor Green
Write-Host "Tente fazer login novamente com:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor Cyan
Write-Host "  Password: admin123" -ForegroundColor Cyan

