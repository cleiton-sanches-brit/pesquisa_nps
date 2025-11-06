"""
Script para gerar um novo link de teste para visualizar templates
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

from django.utils import timezone
from datetime import timedelta
from surveys.models import Survey, SurveyInvitation

def gerar_link_teste():
    """Gera um novo convite para teste"""
    print("=" * 60)
    print("GERANDO NOVO LINK DE TESTE")
    print("=" * 60)
    
    # Buscar a pesquisa de teste
    try:
        survey = Survey.objects.get(id=1)
    except Survey.DoesNotExist:
        print("ERRO: Pesquisa ID 1 nao encontrada!")
        print("Execute primeiro: python criar_dados_teste.py")
        return
    
    # Criar novo convite
    email_teste = f"teste_{timezone.now().strftime('%Y%m%d%H%M%S')}@example.com"
    
    invitation = SurveyInvitation.objects.create(
        survey=survey,
        email=email_teste,
        expires_at=timezone.now() + timedelta(days=30)
    )
    
    # Gerar URL completa
    base_url = "http://localhost:8000"
    url_responder = f"{base_url}/survey/{survey.id}/respond/{invitation.unique_token}/"
    url_lista = f"{base_url}/survey/{survey.id}/invitations/"
    url_enviar = f"{base_url}/survey/{survey.id}/invite/"
    
    print(f"\nNOVO CONVITE CRIADO!")
    print(f"=" * 60)
    print(f"Email: {email_teste}")
    print(f"Token: {invitation.unique_token}")
    print(f"\nURLs para testar:")
    print(f"=" * 60)
    print(f"\n1. RESPONDER PESQUISA (NOVO):")
    print(f"   {url_responder}")
    print(f"\n2. Lista de Convites:")
    print(f"   {url_lista}")
    print(f"\n3. Enviar Convites:")
    print(f"   {url_enviar}")
    print(f"\n4. Admin Django:")
    print(f"   {base_url}/admin/")
    print(f"=" * 60)
    
    return invitation

if __name__ == "__main__":
    gerar_link_teste()
