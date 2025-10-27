#!/usr/bin/env python3
"""
Script para iniciar o ambiente de desenvolvimento
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, cwd=None):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=True, 
            capture_output=True, 
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando: {command}")
        print(f"Erro: {e.stderr}")
        return None

def check_venv():
    """Verifica se o ambiente virtual está ativo"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def main():
    print("🚀 Iniciando ambiente de desenvolvimento...")
    
    # Verificar se estamos no diretório correto
    if not Path("requirements.txt").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Verificar ambiente virtual
    if not check_venv():
        print("⚠️  Ambiente virtual não detectado. Ativando...")
        if os.name == 'nt':  # Windows
            run_command("venv\\Scripts\\activate")
        else:  # Linux/Mac
            run_command("source venv/bin/activate")
    
    # Instalar dependências
    print("📦 Instalando dependências...")
    run_command("pip install -r requirements.txt")
    
    # Verificar se o banco está configurado
    print("🗄️  Verificando configuração do banco...")
    
    # Executar migrações do Django
    print("🔄 Executando migrações do Django...")
    run_command("python manage.py makemigrations", cwd="django_app")
    run_command("python manage.py migrate", cwd="django_app")
    
    print("✅ Ambiente configurado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure o arquivo .env com suas credenciais do banco")
    print("2. Execute: python scripts/start_services.py")
    print("3. Acesse:")
    print("   - Django Admin: http://localhost:8000/admin/")
    print("   - FastAPI Docs: http://localhost:8001/docs")

if __name__ == "__main__":
    main()
