#!/usr/bin/env python3
"""
Script para testar envio de email Microsoft/Office 365
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

def testar_email(email_destino):
    """Testa o envio de email"""
    print("=" * 60)
    print("Teste de Envio de Email - Microsoft/Office 365")
    print("=" * 60)
    print()
    
    # Verificar configurações
    print("Configurações:")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    if not settings.EMAIL_HOST_USER:
        print("ERRO: EMAIL_HOST_USER nao configurado")
        return False
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("ERRO: EMAIL_HOST_PASSWORD nao configurado")
        return False
    
    print(f"Enviando email de teste para: {email_destino}")
    print("Aguarde...")
    print()
    
    try:
        subject = "Teste de Email - Sistema NPS Surveys"
        message = f"""
Este é um email de teste do sistema NPS Surveys.

Se você recebeu este email, a configuração do Microsoft/Office 365 está funcionando corretamente!

Configurações:
- Host: {settings.EMAIL_HOST}
- Porta: {settings.EMAIL_PORT}
- TLS: {settings.EMAIL_USE_TLS}
- Remetente: {settings.DEFAULT_FROM_EMAIL}

Sistema de Pesquisas NPS
        """.strip()
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
            fail_silently=False,
        )
        
        print("=" * 60)
        print("SUCESSO! Email enviado com sucesso!")
        print("=" * 60)
        print()
        print(f"Verifique a caixa de entrada de: {email_destino}")
        print("   (Não esqueça de verificar a pasta de spam)")
        print()
        return True
        
    except Exception as e:
        print("=" * 60)
        print("ERRO ao enviar email!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        print()
        print("Possíveis causas:")
        print("1. Credenciais incorretas (usuário ou senha)")
        print("2. Autenticação de dois fatores ativada (precisa de senha de app)")
        print("3. Firewall bloqueando conexão SMTP")
        print("4. Conta Microsoft bloqueada para apps menos seguros")
        print()
        return False

if __name__ == "__main__":
    # Email de teste padrão (pode ser alterado)
    email_teste = sys.argv[1] if len(sys.argv) > 1 else "csanches@br-itsoftware.com.br"
    
    print(f"Email de destino: {email_teste}")
    print()
    
    sucesso = testar_email(email_teste)
    sys.exit(0 if sucesso else 1)

