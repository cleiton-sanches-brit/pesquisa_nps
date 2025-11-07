#!/usr/bin/env python3
"""
Script para enviar email de teste com link real de resposta da pesquisa
"""
import os
import sys
import django
import random
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'django_app'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from surveys.models import Survey, SurveyInvitation, Respondent
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def enviar_email_teste_convite(email_destino):
    """Envia email de teste com link real de resposta"""
    
    print("=" * 60)
    print("Envio de Email de Teste - Convite de Pesquisa")
    print("=" * 60)
    print()
    
    # Verificar se existe uma pesquisa
    survey = Survey.objects.first()
    if not survey:
        print("ERRO: Nenhuma pesquisa encontrada!")
        print("Por favor, crie uma pesquisa primeiro no Django Admin.")
        return False
    
    print(f"Pesquisa selecionada: {survey.title} (ID: {survey.id})")
    print()
    
    # Produto aleatório
    nome_produto = random.choice(["M4Law", "M-File"])
    print(f"Produto atribuído: {nome_produto}")
    print()
    
    try:
        # Criar ou atualizar respondente
        respondent, created = Respondent.objects.get_or_create(
            email=email_destino,
            defaults={
                'nome_produto': nome_produto,
                'active': True
            }
        )
        
        # Se já existia, atualizar nome_produto
        if not created:
            respondent.nome_produto = nome_produto
            respondent.active = True
            respondent.save()
            print(f"Respondente atualizado")
        else:
            print(f"Respondente criado")
        
        # Criar ou obter convite
        invitation, invitation_created = SurveyInvitation.objects.get_or_create(
            survey=survey,
            email=email_destino,
            defaults={
                'expires_at': timezone.now() + timedelta(days=30)
            }
        )
        
        if not invitation_created:
            print(f"Convite já existe, atualizando...")
            invitation.expires_at = timezone.now() + timedelta(days=30)
            invitation.is_used = False  # Resetar se já foi usado
            invitation.sent_at = None  # Resetar para poder enviar novamente
            invitation.save()
        
        # Construir URLs (usando localhost para teste local)
        # Em produção, usar request.build_absolute_uri()
        base_url = "http://localhost:8000"
        tracking_pixel_url = f"{base_url}/track/email/open/{invitation.unique_token}/"
        tracking_url = f"{base_url}/track/link/click/{invitation.unique_token}/"
        survey_url = f"{base_url}{invitation.get_survey_url()}"
        
        print(f"URL do convite: {survey_url}")
        print()
        
        # Renderizar template de email real
        message = render_to_string('surveys/email_invitation.html', {
            'survey': survey,
            'invitation': invitation,
            'survey_url': survey_url,
            'tracking_url': tracking_url,
            'tracking_pixel_url': tracking_pixel_url,
            'expiration_date': invitation.expires_at,
            'nome_produto': nome_produto
        })
        
        # Enviar email
        subject = f"Convite para Pesquisa: {survey.title}"
        print(f"Enviando email para: {email_destino}")
        print(f"Assunto: {subject}")
        print(f"Produto no email: {nome_produto}")
        print("Aguarde...")
        print()
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
            html_message=message,
            fail_silently=False
        )
        
        # Marcar como enviado
        invitation.mark_as_sent()
        
        print("=" * 60)
        print("SUCESSO! Email de convite enviado!")
        print("=" * 60)
        print()
        print(f"Destinatário: {email_destino}")
        print(f"Produto: {nome_produto}")
        print(f"Link de resposta: {survey_url}")
        print()
        print("Verifique a caixa de entrada (e pasta de spam)")
        print()
        return True
        
    except Exception as e:
        print("=" * 60)
        print("ERRO ao enviar email!")
        print("=" * 60)
        print()
        print(f"Erro: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    email_teste = sys.argv[1] if len(sys.argv) > 1 else "csanches@br-itsoftware.com.br"
    
    print(f"Email de destino: {email_teste}")
    print()
    
    sucesso = enviar_email_teste_convite(email_teste)
    sys.exit(0 if sucesso else 1)

