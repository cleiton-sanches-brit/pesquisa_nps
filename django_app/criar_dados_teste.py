"""
Script para criar dados de teste para validar os templates
"""
import os
import sys
import django
from pathlib import Path

# Configurar caminho
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django ANTES de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

# Agora pode importar modelos
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from surveys.models import Survey, Question, SurveyInvitation, Respondent

def criar_dados_teste():
    """Cria dados de teste para testar os templates"""
    print("=" * 60)
    print("CRIANDO DADOS DE TESTE")
    print("=" * 60)
    
    # Criar ou obter usuário admin
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print("OK: Usuario admin criado (admin/admin123)")
    else:
        print("OK: Usuario admin ja existe")
    
    # Criar pesquisa de teste
    survey, created = Survey.objects.get_or_create(
        title='Pesquisa de Satisfação NPS - Teste',
        defaults={
            'description': 'Esta é uma pesquisa de teste para validar os templates. Por favor, responda com sinceridade.',
            'is_active': True,
            'created_by': user,
            'expires_at': timezone.now() + timedelta(days=30)
        }
    )
    
    if created:
        print(f"OK: Pesquisa criada: {survey.title} (ID: {survey.id})")
        
        # Criar perguntas
        # Pergunta NPS
        q1 = Question.objects.create(
            survey=survey,
            question_text='Em uma escala de 0 a 10, quanto voce recomendaria nossos servicos?',
            question_type='nps',
            is_required=True,
            order=1
        )
        print(f"  OK: Pergunta NPS criada")
        
        # Pergunta de texto
        q2 = Question.objects.create(
            survey=survey,
            question_text='O que podemos fazer para melhorar?',
            question_type='text',
            is_required=False,
            order=2
        )
        print(f"  OK: Pergunta texto criada")
        
        # Pergunta de avaliação
        q3 = Question.objects.create(
            survey=survey,
            question_text='Como voce avalia nossa qualidade?',
            question_type='rating',
            is_required=True,
            order=3
        )
        print(f"  OK: Pergunta rating criada")
    else:
        print(f"OK: Pesquisa ja existe: {survey.title} (ID: {survey.id})")
    
    # Criar respondentes de teste
    respondentes_teste = [
        {'email': 'teste1@example.com', 'nome_usuario': 'João Silva', 'nome_conta': 'Empresa A'},
        {'email': 'teste2@example.com', 'nome_usuario': 'Maria Santos', 'nome_conta': 'Empresa B'},
        {'email': 'teste3@example.com', 'nome_usuario': 'Pedro Costa', 'nome_conta': 'Empresa A'},
    ]
    
    for resp_data in respondentes_teste:
        respondent, created = Respondent.objects.get_or_create(
            email=resp_data['email'],
            defaults={
                'nome_usuario': resp_data['nome_usuario'],
                'nome_conta': resp_data['nome_conta'],
                'status_usuario': 'Ativo'
            }
        )
        if created:
            print(f"OK: Respondente criado: {resp_data['email']}")
    
    # Criar convites de teste
    convites_criados = 0
    for resp_data in respondentes_teste:
        invitation, created = SurveyInvitation.objects.get_or_create(
            survey=survey,
            email=resp_data['email'],
            defaults={
                'expires_at': timezone.now() + timedelta(days=30)
            }
        )
        if created:
            convites_criados += 1
            print(f"OK: Convite criado para: {resp_data['email']}")
            print(f"  Token: {invitation.unique_token}")
            print(f"  URL: /survey/{survey.id}/respond/{invitation.unique_token}/")
    
    print("\n" + "=" * 60)
    print("DADOS DE TESTE CRIADOS COM SUCESSO!")
    print("=" * 60)
    print(f"\nPesquisa ID: {survey.id}")
    print(f"Convites criados: {convites_criados}")
    print(f"\nURLs para testar:")
    print(f"  1. Lista de convites: http://localhost:8000/survey/{survey.id}/invitations/")
    print(f"  2. Enviar convites: http://localhost:8000/survey/{survey.id}/invite/")
    
    if convites_criados > 0:
        invitation = SurveyInvitation.objects.filter(survey=survey).first()
        print(f"  3. Responder pesquisa: http://localhost:8000/survey/{survey.id}/respond/{invitation.unique_token}/")
    
    print(f"\nPara testar templates de erro:")
    print(f"  - Criar convite expirado manualmente")
    print(f"  - Marcar convite como usado")
    
    return survey

if __name__ == "__main__":
    criar_dados_teste()
