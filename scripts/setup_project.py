#!/usr/bin/env python3
"""
Script completo de configuração do projeto NPS Surveys
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check, 
            capture_output=True, 
            text=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {command}")
        print(f"Erro: {e.stderr}")
        return None, e.stderr

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ é necessário")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def setup_environment():
    """Configura o ambiente virtual e instala dependências"""
    print("\n🔧 Configurando ambiente...")
    
    # Criar ambiente virtual se não existir
    if not Path("venv").exists():
        print("📦 Criando ambiente virtual...")
        stdout, stderr = run_command("python -m venv venv")
        if stderr:
            print(f"⚠️  Aviso: {stderr}")
    
    # Ativar ambiente virtual e instalar dependências
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Linux/Mac
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print("📦 Instalando dependências...")
    stdout, stderr = run_command(f"{pip_cmd} install -r requirements.txt")
    if stderr and "ERROR" in stderr:
        print(f"❌ Erro na instalação: {stderr}")
        return False
    
    return True

def setup_database():
    """Configura o banco de dados"""
    print("\n🗄️  Configurando banco de dados...")
    
    # Verificar se .env existe
    if not Path(".env").exists():
        if Path("env.example").exists():
            shutil.copy("env.example", ".env")
            print("📝 Arquivo .env criado a partir do exemplo")
            print("⚠️  Configure suas credenciais do banco no arquivo .env")
        else:
            print("❌ Arquivo env.example não encontrado")
            return False
    
    return True

def run_django_migrations():
    """Executa as migrações do Django"""
    print("\n🔄 Executando migrações do Django...")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Linux/Mac
        python_cmd = "venv/bin/python"
    
    # Criar migrações
    stdout, stderr = run_command(f"{python_cmd} manage.py makemigrations", cwd="dashboard")
    if stderr and "ERROR" in stderr:
        print(f"⚠️  Aviso nas migrações: {stderr}")
    
    # Aplicar migrações
    stdout, stderr = run_command(f"{python_cmd} manage.py migrate", cwd="dashboard")
    if stderr and "ERROR" in stderr:
        print(f"⚠️  Aviso nas migrações: {stderr}")
    
    return True

def create_superuser():
    """Cria um superusuário do Django"""
    print("\n👤 Criando superusuário...")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Linux/Mac
        python_cmd = "venv/bin/python"
    
    # Verificar se já existe superusuário
    stdout, stderr = run_command(
        f"{python_cmd} manage.py shell -c \"from django.contrib.auth.models import User; print('Superuser exists' if User.objects.filter(is_superuser=True).exists() else 'No superuser')\"",
        cwd="dashboard",
        check=False
    )
    
    if "No superuser" in stdout:
        print("📝 Crie um superusuário manualmente com:")
        print(f"   {python_cmd} manage.py createsuperuser")
    else:
        print("✅ Superusuário já existe")
    
    return True

def main():
    print("🚀 Configuração do Projeto NPS Surveys")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Configurar ambiente
    if not setup_environment():
        print("❌ Falha na configuração do ambiente")
        sys.exit(1)
    
    # Configurar banco
    if not setup_database():
        print("❌ Falha na configuração do banco")
        sys.exit(1)
    
    # Executar migrações
    if not run_django_migrations():
        print("❌ Falha nas migrações")
        sys.exit(1)
    
    # Criar superusuário
    create_superuser()
    
    print("\n🎉 Configuração concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure suas credenciais do banco no arquivo .env")
    print("2. Teste a conexão: python scripts/test_db_connection.py")
    print("3. Inicie os serviços: python scripts/start_services.py")
    print("\n🌐 URLs importantes:")
    print("   - Django Admin: http://localhost:8000/admin/")
    print("   - FastAPI Docs: http://localhost:8001/docs")

if __name__ == "__main__":
    main()
