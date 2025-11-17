"""
Script para atualizar as perguntas conforme solicitado
"""
import os
import sys
import django
from pathlib import Path

# Configurar caminho
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from surveys.models import Survey, Question, Choice

def atualizar_perguntas():
    """Atualiza as perguntas conforme solicitado"""
    print("=" * 60)
    print("ATUALIZANDO PERGUNTAS")
    print("=" * 60)
    
    try:
        survey = Survey.objects.get(id=1)
    except Survey.DoesNotExist:
        print("ERRO: Pesquisa ID 1 nao encontrada!")
        return
    
    # 1. Atualizar título da pesquisa
    survey.title = "Pesquisa de Satisfação"
    survey.save()
    print("OK: Titulo da pesquisa atualizado para 'Pesquisa de Satisfacao'")
    
    # 2. Atualizar pergunta de texto
    try:
        q_text = Question.objects.get(survey=survey, question_type='text')
        q_text.question_text = "Comente sobre o que motivou sua nota"
        q_text.save()
        print("OK: Pergunta de texto atualizada")
    except Question.DoesNotExist:
        print("AVISO: Pergunta de texto nao encontrada")
    
    # 3. Alterar pergunta de rating para checkbox (choice)
    try:
        q_rating = Question.objects.get(survey=survey, question_type='rating')
        
        # Mudar tipo para choice
        q_rating.question_type = 'choice'
        q_rating.question_text = "Deseja receber contato da nossa equipe?"
        q_rating.is_required = False  # Checkbox geralmente não é obrigatório
        q_rating.save()
        print("OK: Pergunta de rating alterada para choice (checkbox)")
        
        # Criar opções para o checkbox (Sim/Não)
        # Deletar choices antigas se existirem
        Choice.objects.filter(question=q_rating).delete()
        
        # Criar novas opções
        Choice.objects.create(
            question=q_rating,
            choice_text="Sim, desejo receber contato",
            value="sim",
            order=1
        )
        Choice.objects.create(
            question=q_rating,
            choice_text="Não, não desejo receber contato",
            value="nao",
            order=2
        )
        print("OK: Opcoes de checkbox criadas (Sim/Nao)")
        
    except Question.DoesNotExist:
        print("AVISO: Pergunta de rating nao encontrada")
    
    print("\n" + "=" * 60)
    print("ATUALIZACAO CONCLUIDA!")
    print("=" * 60)
    print("\nReinicie o servidor Django para ver as alteracoes.")
    print("\nNovo link para testar:")
    print("http://localhost:8000/survey/1/respond/[TOKEN]/")

if __name__ == "__main__":
    atualizar_perguntas()
