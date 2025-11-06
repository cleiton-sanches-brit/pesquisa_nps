#!/usr/bin/env python3
"""
Script para criar e aplicar migração do campo nome_produto
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'django_app'))
os.chdir(BASE_DIR / 'django_app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.core.management import call_command

def main():
    print("=" * 60)
    print("Criando e Aplicando Migração - Campo nome_produto")
    print("=" * 60)
    print()
    
    try:
        # 1. Criar migração
        print("1. Criando migração...")
        call_command('makemigrations', 'surveys', verbosity=2)
        print("   OK - Migração criada com sucesso!")
        print()
        
        # 2. Aplicar migração
        print("2. Aplicando migração...")
        call_command('migrate', 'surveys', verbosity=2)
        print("   OK - Migração aplicada com sucesso!")
        print()
        
        print("=" * 60)
        print("SUCESSO! Campo nome_produto adicionado ao banco de dados")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("1. Acesse Django Admin")
        print("2. Vá em 'Respondentes'")
        print("3. Crie ou edite um respondente")
        print("4. Preencha o campo 'Nome do Produto'")
        print("5. Envie convite para testar")
        print()
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("ERRO ao executar migração!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário")
        sys.exit(1)

