"""
Utilitários para cálculo e processamento de NPS
"""
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Survey, SurveyResponse, Answer, NPSResult, Question
from decimal import Decimal


def calculate_nps_from_responses(responses, nps_questions):
    """
    Calcula NPS a partir de respostas e perguntas NPS
    
    Args:
        responses: QuerySet de SurveyResponse
        nps_questions: QuerySet de Question (tipo 'nps')
    
    Returns:
        dict com: total_responses, promoters, passives, detractors, nps_score
    """
    total_responses = 0
    promoters = 0
    passives = 0
    detractors = 0
    
    for response in responses:
        for nps_question in nps_questions:
            answer = response.answers.filter(question=nps_question).first()
            if answer and answer.answer_value:
                try:
                    score = int(answer.answer_value)
                    total_responses += 1
                    
                    if score >= 9:
                        promoters += 1
                    elif score >= 7:
                        passives += 1
                    else:
                        detractors += 1
                    
                    # Pegar apenas uma resposta NPS por response
                    break
                except (ValueError, TypeError):
                    continue
    
    # Calcular score NPS
    if total_responses > 0:
        nps_score = Decimal(((promoters - detractors) / total_responses) * 100)
        nps_score = round(nps_score, 2)
    else:
        nps_score = Decimal('0.00')
    
    return {
        'total_responses': total_responses,
        'promoters': promoters,
        'passives': passives,
        'detractors': detractors,
        'nps_score': nps_score
    }


def calculate_and_save_nps(survey, period_start=None, period_end=None, force_recalculate=False):
    """
    Calcula e salva resultado NPS para uma pesquisa e período
    
    Args:
        survey: Objeto Survey
        period_start: Data inicial (datetime.date). Se None, usa início do mês atual
        period_end: Data final (datetime.date). Se None, usa fim do mês atual
        force_recalculate: Se True, recalcula mesmo se já existir resultado
    
    Returns:
        NPSResult object ou None se não houver respostas
    """
    # Definir período padrão se não fornecido
    now = timezone.now().date()
    if period_start is None:
        period_start = now.replace(day=1)
    if period_end is None:
        # Último dia do mês
        if now.month == 12:
            period_end = now.replace(day=31)
        else:
            next_month = now.replace(month=now.month + 1, day=1)
            period_end = (next_month - timedelta(days=1))
    
    # Verificar se já existe resultado
    if not force_recalculate:
        existing_result = NPSResult.objects.filter(
            survey=survey,
            period_start=period_start,
            period_end=period_end
        ).first()
        
        if existing_result:
            return existing_result
    
    # Buscar respostas do período
    responses = survey.responses.filter(
        submitted_at__date__range=[period_start, period_end]
    )
    
    # Buscar perguntas NPS
    nps_questions = survey.questions.filter(question_type='nps')
    
    if not nps_questions.exists():
        return None
    
    # Calcular NPS
    nps_data = calculate_nps_from_responses(responses, nps_questions)
    
    if nps_data['total_responses'] == 0:
        return None
    
    # Criar ou atualizar resultado
    nps_result, created = NPSResult.objects.update_or_create(
        survey=survey,
        period_start=period_start,
        period_end=period_end,
        defaults={
            'total_responses': nps_data['total_responses'],
            'promoters': nps_data['promoters'],
            'passives': nps_data['passives'],
            'detractors': nps_data['detractors'],
            'nps_score': nps_data['nps_score']
        }
    )
    
    return nps_result


def get_nps_summary(survey=None, period_start=None, period_end=None):
    """
    Obtém resumo NPS agregado
    
    Args:
        survey: Objeto Survey (opcional). Se None, agrega todas as pesquisas
        period_start: Data inicial (opcional)
        period_end: Data final (opcional)
    
    Returns:
        dict com resumo agregado
    """
    if survey:
        surveys = [survey]
    else:
        surveys = Survey.objects.filter(is_active=True)
    
    total_responses = 0
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    
    for s in surveys:
        responses = s.responses.all()
        if period_start and period_end:
            responses = responses.filter(
                submitted_at__date__range=[period_start, period_end]
            )
        
        nps_questions = s.questions.filter(question_type='nps')
        if nps_questions.exists():
            nps_data = calculate_nps_from_responses(responses, nps_questions)
            total_responses += nps_data['total_responses']
            total_promoters += nps_data['promoters']
            total_passives += nps_data['passives']
            total_detractors += nps_data['detractors']
    
    if total_responses > 0:
        nps_score = Decimal(((total_promoters - total_detractors) / total_responses) * 100)
        nps_score = round(nps_score, 2)
    else:
        nps_score = Decimal('0.00')
    
    return {
        'total_responses': total_responses,
        'promoters': total_promoters,
        'passives': total_passives,
        'detractors': total_detractors,
        'nps_score': nps_score,
        'promoter_percentage': round((total_promoters / total_responses * 100), 2) if total_responses > 0 else 0,
        'passive_percentage': round((total_passives / total_responses * 100), 2) if total_responses > 0 else 0,
        'detractor_percentage': round((total_detractors / total_responses * 100), 2) if total_responses > 0 else 0,
    }


def get_nps_trend_data(survey, months=6):
    """
    Obtém dados de tendência NPS para gráficos
    
    Args:
        survey: Objeto Survey
        months: Número de meses para retornar
    
    Returns:
        list de dicts com dados mensais
    """
    now = timezone.now().date()
    trend_data = []
    
    for i in range(months - 1, -1, -1):
        month_date = now - timedelta(days=30 * i)
        period_start = month_date.replace(day=1)
        
        # Último dia do mês
        if month_date.month == 12:
            period_end = month_date.replace(day=31)
        else:
            next_month = month_date.replace(month=month_date.month + 1, day=1)
            period_end = (next_month - timedelta(days=1))
        
        # Buscar ou calcular resultado
        nps_result = NPSResult.objects.filter(
            survey=survey,
            period_start=period_start,
            period_end=period_end
        ).first()
        
        if not nps_result:
            # Calcular se não existir
            nps_result = calculate_and_save_nps(survey, period_start, period_end)
        
        if nps_result:
            trend_data.append({
                'period': period_start.strftime('%Y-%m'),
                'period_start': period_start,
                'period_end': period_end,
                'nps_score': float(nps_result.nps_score),
                'total_responses': nps_result.total_responses,
                'promoters': nps_result.promoters,
                'passives': nps_result.passives,
                'detractors': nps_result.detractors,
            })
        else:
            trend_data.append({
                'period': period_start.strftime('%Y-%m'),
                'period_start': period_start,
                'period_end': period_end,
                'nps_score': 0,
                'total_responses': 0,
                'promoters': 0,
                'passives': 0,
                'detractors': 0,
            })
    
    return trend_data

