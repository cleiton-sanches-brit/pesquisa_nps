#!/usr/bin/env python
"""
Script para criar usuário administrador no Django quando hospedado no Azure App Service.

Este script pode ser executado via:
1. Console SSH do Azure Portal
2. Azure CLI (az webapp ssh)
3. Qualquer terminal com acesso ao servidor

Uso:
    python criar_admin_azure.py

Ou com variáveis de ambiente:
    export ADMIN_USERNAME=admin
    export ADMIN_EMAIL=admin@example.com
    export ADMIN_PASSWORD=SenhaSegura123!
    python criar_admin_azure.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')

try:
    django.setup()
except Exception as e:
    print(f"ERRO ao configurar Django: {e}")
    print("\nCertifique-se de estar na pasta django_app e que o Django está instalado.")
    sys.exit(1)

from django.contrib.auth import get_user_model

User = get_user_model()


def criar_superusuario():
    """Cria ou atualiza um superusuário no Django"""
    
    # Obter valores das variáveis de ambiente ou usar padrões
    username = os.getenv('ADMIN_USERNAME', 'admin')
    email = os.getenv('ADMIN_EMAIL', 'admin@br-itsoftware.com.br')
    password = os.getenv('ADMIN_PASSWORD')
    
    # Se não houver senha nas variáveis de ambiente, solicitar interativamente
    if not password:
        print("=" * 60)
        print("CRIAR USUÁRIO ADMINISTRADOR - Django")
        print("=" * 60)
        print()
        print("Este script criará ou atualizará um superusuário.")
        print()
        
        # Solicitar informações
        username = input(f"Username [{username}]: ").strip() or username
        email = input(f"Email [{email}]: ").strip() or email
        
        import getpass
        password = getpass.getpass("Password: ")
        password_confirm = getpass.getpass("Password (again): ")
        
        if password != password_confirm:
            print("\nERRO: As senhas não coincidem!")
            sys.exit(1)
        
        if len(password) < 8:
            print("\nAVISO: Senha muito curta. Recomendado mínimo de 12 caracteres.")
            continuar = input("Deseja continuar mesmo assim? (s/N): ").strip().lower()
            if continuar != 's':
                sys.exit(0)
    
    # Verificar se o usuário já existe
    if User.objects.filter(username=username).exists():
        print(f"\n⚠️  Usuário '{username}' já existe!")
        opcao = input("Deseja atualizar a senha? (s/N): ").strip().lower()
        
        if opcao == 's':
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            print(f"\n✅ Senha do usuário '{username}' foi atualizada com sucesso!")
            print(f"   Email: {email}")
            return True
        else:
            print("Operação cancelada.")
            return False
    else:
        # Criar novo superusuário
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"\n✅ Superusuário '{username}' criado com sucesso!")
            print(f"   Email: {email}")
            print(f"\n🌐 Acesse o admin em: https://seu-app.azurewebsites.net/admin/")
            return True
        except Exception as e:
            print(f"\n❌ ERRO ao criar superusuário: {e}")
            return False


def main():
    """Função principal"""
    try:
        # Verificar se as migrações foram executadas
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'auth_user'")
            tabela_existe = cursor.fetchone()[0] > 0
        
        if not tabela_existe:
            print("⚠️  AVISO: A tabela 'auth_user' não existe!")
            print("   Execute primeiro: python manage.py migrate")
            sys.exit(1)
        
        # Criar superusuário
        sucesso = criar_superusuario()
        
        if sucesso:
            print("\n" + "=" * 60)
            print("✅ Processo concluído com sucesso!")
            print("=" * 60)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique:")
        print("1. Se está na pasta django_app")
        print("2. Se as migrações foram executadas")
        print("3. Se o banco de dados está acessível")
        print("4. Se as variáveis de ambiente estão configuradas")
        sys.exit(1)


if __name__ == '__main__':
    main()

