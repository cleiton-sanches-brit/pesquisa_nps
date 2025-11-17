"""
Script para testar se as URLs estão configuradas corretamente
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.urls import reverse
from django.test import Client

def test_urls():
    """Testa se as URLs estão configuradas"""
    print("=" * 60)
    print("TESTANDO URLs DE CONVITES")
    print("=" * 60)
    
    client = Client()
    
    # Lista de URLs para testar
    urls_to_test = [
        ('survey_invitations', {'survey_id': 1}),
        ('send_survey_invitations', {'survey_id': 1}),
        ('resend_invitation', {'invitation_id': 1}),
    ]
    
    print("\nTestando URLs...")
    for url_name, kwargs in urls_to_test:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"OK: {url_name} -> {url}")
        except Exception as e:
            print(f"ERRO: {url_name} - {str(e)}")
    
    # Testar URL de resposta (precisa de token UUID)
    try:
        from uuid import uuid4
        test_token = uuid4()
        url = reverse('respond_survey', kwargs={'survey_id': 1, 'token': test_token})
        print(f"OK: respond_survey -> {url[:50]}...")
    except Exception as e:
        print(f"ERRO: respond_survey - {str(e)}")
    
    print("\n" + "=" * 60)
    print("Teste concluido!")
    print("=" * 60)

if __name__ == "__main__":
    test_urls()
