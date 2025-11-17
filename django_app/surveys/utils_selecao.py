"""
Utilitários para seleção automática de convidados para pesquisas
"""
from django.utils import timezone
from datetime import timedelta
from .models import Respondent, SurveyInvitation
import random


def selecionar_convidados_automatico(survey_id, percentual=1/6):
    """
    Seleciona automaticamente convidados para uma pesquisa baseado nos critérios:
    - Seleciona aleatoriamente uma porcentagem do total (padrão: 1/6 = 16.67%)
    - Exclui emails que receberam convite nos últimos 180 dias
    
    Args:
        survey_id: ID da pesquisa
        percentual: Percentual a selecionar (padrão: 1/6 = 0.1667)
    
    Returns:
        tuple: (lista de emails selecionados, total disponível, total excluídos)
    """
    # Data limite: 180 dias atrás
    data_limite = timezone.now() - timedelta(days=180)
    
    # Buscar todos os respondentes ativos
    respondentes_ativos = Respondent.objects.filter(active=True)
    total_respondentes = respondentes_ativos.count()
    
    # Lista de emails que NÃO podem ser convidados (receberam convite nos últimos 180 dias)
    emails_excluidos = set()
    
    # Buscar todos os convites enviados nos últimos 180 dias (de qualquer pesquisa)
    convites_recentes = SurveyInvitation.objects.filter(
        sent_at__gte=data_limite
    ).exclude(sent_at__isnull=True)
    
    # Adicionar emails que receberam convite recente
    for convite in convites_recentes:
        emails_excluidos.add(convite.email.lower())
    
    # Filtrar respondentes elegíveis (ativos e não receberam convite recente)
    respondentes_elegiveis = []
    for respondente in respondentes_ativos:
        email_lower = respondente.email.lower()
        if email_lower not in emails_excluidos:
            respondentes_elegiveis.append(respondente.email)
    
    total_elegiveis = len(respondentes_elegiveis)
    total_excluidos = len(emails_excluidos)
    
    # Calcular quantos selecionar (1/6 do total elegível)
    quantidade_selecionar = max(1, int(total_elegiveis * percentual))
    
    # Selecionar aleatoriamente
    if total_elegiveis > 0:
        emails_selecionados = random.sample(respondentes_elegiveis, min(quantidade_selecionar, total_elegiveis))
    else:
        emails_selecionados = []
    
    return {
        'emails_selecionados': emails_selecionados,
        'total_respondentes': total_respondentes,
        'total_elegiveis': total_elegiveis,
        'total_excluidos': total_excluidos,
        'quantidade_selecionada': len(emails_selecionados),
        'percentual_usado': percentual
    }


def validar_email_pode_ser_convidado(email, survey_id=None):
    """
    Valida se um email pode receber um novo convite
    (não recebeu convite nos últimos 180 dias)
    
    Args:
        email: Email a validar
        survey_id: ID da pesquisa (opcional, para validação específica)
    
    Returns:
        tuple: (pode_ser_convidado: bool, motivo: str)
    """
    data_limite = timezone.now() - timedelta(days=180)
    
    # Buscar convites recentes para este email
    query = SurveyInvitation.objects.filter(
        email__iexact=email,
        sent_at__gte=data_limite
    ).exclude(sent_at__isnull=True)
    
    if survey_id:
        query = query.filter(survey_id=survey_id)
    
    convite_recente = query.order_by('-sent_at').first()
    
    if convite_recente:
        dias_desde_envio = (timezone.now() - convite_recente.sent_at).days
        return False, f"Recebeu convite há {dias_desde_envio} dias (limite: 180 dias)"
    
    return True, "Email elegível para convite"


def criar_convites_automaticos(survey_id, percentual=1/6):
    """
    Cria convites automaticamente para uma pesquisa seguindo os critérios definidos
    
    Args:
        survey_id: ID da pesquisa
        percentual: Percentual a selecionar (padrão: 1/6)
    
    Returns:
        dict: Resultado da operação com estatísticas
    """
    from .models import Survey
    
    try:
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        return {
            'sucesso': False,
            'erro': f'Pesquisa com ID {survey_id} não encontrada'
        }
    
    # Selecionar emails elegíveis
    resultado_selecao = selecionar_convidados_automatico(survey_id, percentual)
    
    emails_selecionados = resultado_selecao['emails_selecionados']
    convites_criados = []
    convites_ja_existentes = []
    erros = []
    
    # Criar convites para cada email selecionado
    for email in emails_selecionados:
        try:
            # Verificar se já existe convite para esta pesquisa
            convite_existente = SurveyInvitation.objects.filter(
                survey=survey,
                email=email
            ).first()
            
            if convite_existente:
                convites_ja_existentes.append(email)
                continue
            
            # Criar novo convite (expira em 30 dias)
            from datetime import timedelta
            invitation = SurveyInvitation.objects.create(
                survey=survey,
                email=email,
                expires_at=timezone.now() + timedelta(days=30)
            )
            convites_criados.append(email)
            
        except Exception as e:
            erros.append(f"{email}: {str(e)}")
    
    return {
        'sucesso': True,
        'survey': survey.title,
        'total_respondentes': resultado_selecao['total_respondentes'],
        'total_elegiveis': resultado_selecao['total_elegiveis'],
        'total_excluidos': resultado_selecao['total_excluidos'],
        'emails_selecionados': len(emails_selecionados),
        'convites_criados': len(convites_criados),
        'convites_ja_existentes': len(convites_ja_existentes),
        'erros': len(erros),
        'lista_emails': emails_selecionados,
        'detalhes_erros': erros
    }

