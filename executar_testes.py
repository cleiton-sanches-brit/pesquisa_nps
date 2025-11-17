#!/usr/bin/env python3
"""
Script para executar testes do Django
"""
import os
import sys

# Adicionar django_app ao path
django_app_path = os.path.join(os.path.dirname(__file__), 'django_app')
sys.path.insert(0, django_app_path)

# Mudar para o diretório django_app
os.chdir(django_app_path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')

import django
django.setup()

from django.core.management import call_command

if __name__ == "__main__":
    print("=" * 60)
    print("Executando Testes do Sistema NPS Surveys")
    print("=" * 60)
    print()
    
    # Executar testes
    try:
        call_command('test', 'surveys', verbosity=2)
    except Exception as e:
        print(f"\nErro ao executar testes: {e}")
        sys.exit(1)

