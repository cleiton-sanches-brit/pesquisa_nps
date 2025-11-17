#!/usr/bin/env python3
"""
Script para testar o envio de emails do sistema NPS Surveys
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'django_app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def test_email_config():
    """Testa a configuração de email"""
    print("=" * 60)
    print("Teste de Configuracao de Email - NPS Surveys")
    print("=" * 60)
    print()
    
    # Verificar configurações
    print("Verificando configuracoes...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    # Verificar se as credenciais estão configuradas
    if not settings.EMAIL_HOST_USER:
        print("ERRO: EMAIL_HOST_USER nao configurado no .env")
        print("Adicione EMAIL_HOST_USER=seu-email@gmail.com no arquivo .env")
        return False
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("ERRO: EMAIL_HOST_PASSWORD nao configurado no .env")
        print("Adicione EMAIL_HOST_PASSWORD=sua-senha no arquivo .env")
        return False
    
    print("OK - Configuracoes encontradas")
    print()
    
    # Solicitar email de teste
    print("Para testar o envio, informe:")
    email_destino = input("Email de destino para teste (ou Enter para pular): ").strip()
    
    if not email_destino:
        print("\nTeste cancelado. Para testar depois, execute:")
        print("python testar_envio_email.py")
        return True
    
    # Validar email
    if '@' not in email_destino:
        print(f"ERRO: Email invalido: {email_destino}")
        return False
    
    print()
    print(f"Enviando email de teste para: {email_destino}")
    print("Aguarde...")
    print()
    
    try:
        # Criar email de teste simples
        subject = "Teste de Email - NPS Surveys"
        message_plain = """
        Este e um email de teste do sistema NPS Surveys.
        
        Se voce recebeu este email, a configuracao esta funcionando corretamente!
        
        Configuracoes:
        - Host: {host}
        - Porta: {port}
        - TLS: {tls}
        - Usuario: {user}
        """.format(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            tls=settings.EMAIL_USE_TLS,
            user=settings.EMAIL_HOST_USER
        )
        
        send_mail(
            subject,
            message_plain,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
            fail_silently=False,
        )
        
        print("=" * 60)
        print("SUCESSO! Email enviado com sucesso!")
        print("=" * 60)
        print()
        print(f"Verifique a caixa de entrada de: {email_destino}")
        print("(Nao esqueca de verificar a pasta de spam)")
        print()
        return True
        
    except Exception as e:
        print("=" * 60)
        print("ERRO ao enviar email!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        print()
        print("Possiveis causas:")
        print("1. Credenciais incorretas (EMAIL_HOST_USER ou EMAIL_HOST_PASSWORD)")
        print("2. Para Gmail: precisa usar 'Senha de App', nao senha normal")
        print("3. Porta ou TLS configurados incorretamente")
        print("4. Firewall bloqueando conexao SMTP")
        print()
        print("Consulte GUIA_CONFIGURACAO_EMAIL.md para mais detalhes")
        return False

if __name__ == "__main__":
    try:
        success = test_email_config()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTeste cancelado pelo usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

