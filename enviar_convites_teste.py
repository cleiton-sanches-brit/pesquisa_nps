#!/usr/bin/env python3
"""
Script para enviar convites de teste com nome do produto aleatório
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
from django.http import HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def enviar_convites_teste():
    """Envia convites de teste para os emails fornecidos"""
    
    print("=" * 60)
    print("Envio de Convites de Teste - NPS Surveys")
    print("=" * 60)
    print()
    
    # Emails e produtos aleatórios
    emails_produtos = [
        ("csanches@br-itsoftware.com.br", random.choice(["M4Law", "M-File"])),
        ("apereira@br-itsoftware.com.br", random.choice(["M4Law", "M-File"]))
    ]
    
    # Verificar se existe uma pesquisa
    survey = Survey.objects.first()
    if not survey:
        print("ERRO: Nenhuma pesquisa encontrada!")
        print("Por favor, crie uma pesquisa primeiro no Django Admin.")
        return False
    
    print(f"Pesquisa selecionada: {survey.title} (ID: {survey.id})")
    print()
    
    # Criar/atualizar respondentes e enviar convites
    resultados = []
    
    for email, nome_produto in emails_produtos:
        print(f"Processando: {email}")
        print(f"  Produto: {nome_produto}")
        
        try:
            # Criar ou atualizar respondente
            respondent, created = Respondent.objects.get_or_create(
                email=email,
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
                print(f"  Respondente atualizado")
            else:
                print(f"  Respondente criado")
            
            # Verificar se já existe convite
            invitation, invitation_created = SurveyInvitation.objects.get_or_create(
                survey=survey,
                email=email,
                defaults={
                    'expires_at': timezone.now() + timedelta(days=30)
                }
            )
            
            if not invitation_created:
                print(f"  AVISO: Convite já existe para este email")
                # Atualizar data de expiração
                invitation.expires_at = timezone.now() + timedelta(days=30)
                invitation.save()
            
            # Construir URLs (usando localhost para teste)
            # Em produção, usar request.build_absolute_uri()
            base_url = "http://localhost:8000"
            tracking_pixel_url = f"{base_url}/track/email/open/{invitation.unique_token}/"
            tracking_url = f"{base_url}/track/link/click/{invitation.unique_token}/"
            survey_url = f"{base_url}{invitation.get_survey_url()}"
            
            # Renderizar template de email
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
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
                fail_silently=False
            )
            
            # Marcar como enviado
            invitation.mark_as_sent()
            
            print(f"  [OK] Email enviado com sucesso!")
            resultados.append({
                'email': email,
                'produto': nome_produto,
                'status': 'sucesso',
                'invitation_id': invitation.id
            })
            
        except Exception as e:
            print(f"  [ERRO] {str(e)}")
            resultados.append({
                'email': email,
                'produto': nome_produto,
                'status': 'erro',
                'erro': str(e)
            })
        
        print()
    
    # Resumo
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    print()
    
    sucessos = [r for r in resultados if r['status'] == 'sucesso']
    erros = [r for r in resultados if r['status'] == 'erro']
    
    print(f"[OK] Enviados com sucesso: {len(sucessos)}")
    for r in sucessos:
        print(f"   - {r['email']} (Produto: {r['produto']})")
    
    if erros:
        print()
        print(f"[ERRO] Erros: {len(erros)}")
        for r in erros:
            print(f"   - {r['email']}: {r.get('erro', 'Erro desconhecido')}")
    
    print()
    print("=" * 60)
    
    return len(erros) == 0

if __name__ == "__main__":
    try:
        sucesso = enviar_convites_teste()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERRO FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

