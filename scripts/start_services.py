#!/usr/bin/env python3
"""
Script para iniciar os serviços Django e FastAPI
"""
import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_django():
    """Executa o servidor Django"""
    print("🐍 Iniciando Django (porta 8000)...")
    os.chdir("dashboard")
    subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

def run_fastapi():
    """Executa o servidor FastAPI"""
    print("⚡ Iniciando FastAPI (porta 8001)...")
    os.chdir("collector")
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])

def main():
    print("🚀 Iniciando serviços...")
    
    # Verificar se estamos no diretório correto
    if not Path("requirements.txt").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Verificar arquivo .env
    if not Path(".env").exists():
        print("⚠️  Arquivo .env não encontrado. Copiando do exemplo...")
        if Path("env.example").exists():
            import shutil
            shutil.copy("env.example", ".env")
            print("📝 Arquivo .env criado. Configure suas credenciais do banco.")
        else:
            print("❌ Arquivo env.example não encontrado")
            sys.exit(1)
    
    try:
        # Iniciar Django em thread separada
        django_thread = threading.Thread(target=run_django)
        django_thread.daemon = True
        django_thread.start()
        
        # Aguardar um pouco para o Django inicializar
        time.sleep(3)
        
        # Iniciar FastAPI em thread separada
        fastapi_thread = threading.Thread(target=run_fastapi)
        fastapi_thread.daemon = True
        fastapi_thread.start()
        
        print("\n✅ Serviços iniciados!")
        print("🌐 Acesse:")
        print("   - Django Admin: http://localhost:8000/admin/")
        print("   - FastAPI Docs: http://localhost:8001/docs")
        print("\n⏹️  Pressione Ctrl+C para parar os serviços")
        
        # Manter o script rodando
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Parando serviços...")
        sys.exit(0)

if __name__ == "__main__":
    main()
