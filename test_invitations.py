#!/usr/bin/env python3
"""
Script para testar o sistema de convites únicos
"""
import os
import sys
import django
from datetime import timedelta

# Configurar Django
sys.path.append('django_app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from surveys.models import Survey, SurveyInvitation, Question, Choice
from django.contrib.auth.models import User
from django.utils import timezone

def create_test_survey():
    """Cria uma pesquisa de teste"""
    print("Criando pesquisa de teste...")
    
    # Criar usuário se não existir
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        user.set_password('admin123')
        user.save()
    
    # Criar pesquisa
    survey, created = Survey.objects.get_or_create(
        title='Pesquisa de Satisfação - Teste',
        defaults={
            'description': 'Esta é uma pesquisa de teste para validar o sistema de convites únicos',
            'created_by': user,
            'expires_at': timezone.now() + timedelta(days=30)
        }
    )
    
    if created:
        print(f"✅ Pesquisa criada: {survey.title}")
        
        # Criar perguntas
        questions_data = [
            {
                'text': 'Qual a probabilidade de você recomendar nosso produto para um amigo?',
                'type': 'nps',
                'required': True
            },
            {
                'text': 'Qual o principal motivo da sua avaliação?',
                'type': 'choice',
                'required': True,
                'choices': [
                    'Qualidade do produto',
                    'Atendimento ao cliente',
                    'Preço',
                    'Facilidade de uso',
                    'Outros'
                ]
            },
            {
                'text': 'Comentários adicionais:',
                'type': 'text',
                'required': False
            }
        ]
        
        for i, q_data in enumerate(questions_data):
            question = Question.objects.create(
                survey=survey,
                question_text=q_data['text'],
                question_type=q_data['type'],
                is_required=q_data['required'],
                order=i + 1
            )
            
            # Criar opções para múltipla escolha
            if q_data['type'] == 'choice':
                for j, choice_text in enumerate(q_data['choices']):
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        value=str(j + 1),
                        order=j + 1
                    )
            
            print(f"  ✅ Pergunta criada: {question.question_text[:50]}...")
    else:
        print(f"✅ Pesquisa já existe: {survey.title}")
    
    return survey

def create_test_invitations(survey):
    """Cria convites de teste"""
    print("\nCriando convites de teste...")
    
    test_emails = [
        'teste1@example.com',
        'teste2@example.com',
        'teste3@example.com'
    ]
    
    for email in test_emails:
        invitation, created = SurveyInvitation.objects.get_or_create(
            survey=survey,
            email=email,
            defaults={
                'expires_at': timezone.now() + timedelta(days=7)
            }
        )
        
        if created:
            print(f"  ✅ Convite criado para: {email}")
            print(f"     Token: {invitation.unique_token}")
            print(f"     URL: /survey/{survey.id}/respond/{invitation.unique_token}/")
        else:
            print(f"  ✅ Convite já existe para: {email}")
    
    return SurveyInvitation.objects.filter(survey=survey)

def test_invitation_validation():
    """Testa a validação de convites"""
    print("\nTestando validação de convites...")
    
    invitations = SurveyInvitation.objects.all()
    
    for invitation in invitations:
        print(f"\nConvite: {invitation.email}")
        print(f"  Token: {invitation.unique_token}")
        print(f"  Válido: {invitation.is_valid()}")
        print(f"  Usado: {invitation.is_used}")
        print(f"  Expira em: {invitation.expires_at}")
        print(f"  URL: {invitation.get_survey_url()}")

def main():
    print("🧪 Teste do Sistema de Convites Únicos")
    print("=" * 50)
    
    # Criar pesquisa de teste
    survey = create_test_survey()
    
    # Criar convites de teste
    invitations = create_test_invitations(survey)
    
    # Testar validação
    test_invitation_validation()
    
    print("\n✅ Teste concluído!")
    print("\n📋 Próximos passos:")
    print("1. Execute as migrações: python manage.py makemigrations && python manage.py migrate")
    print("2. Inicie o servidor: python manage.py runserver")
    print("3. Acesse o admin: http://localhost:8000/admin/")
    print("4. Teste os convites com as URLs geradas")

if __name__ == "__main__":
    main()

