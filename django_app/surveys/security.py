"""
Utilitários de segurança para proteção contra spam e validação
"""
from django.core.cache import cache
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import re


def validate_email_format(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def check_ip_reputation(ip):
    """
    Verifica reputação do IP (simplificado)
    Em produção, pode integrar com serviços como AbuseIPDB
    """
    # Verificar se IP está em blacklist local
    blacklist_key = f'ip_blacklist:{ip}'
    if cache.get(blacklist_key):
        return False
    
    # Verificar quantidade de tentativas falhas deste IP
    failed_attempts_key = f'failed_attempts:{ip}'
    failed_attempts = cache.get(failed_attempts_key, 0)
    
    if failed_attempts > 10:  # Mais de 10 tentativas falhas
        # Adicionar à blacklist temporária (1 hora)
        cache.set(blacklist_key, True, 3600)
        return False
    
    return True


def record_failed_attempt(ip):
    """Registra tentativa falha de IP"""
    failed_attempts_key = f'failed_attempts:{ip}'
    failed_attempts = cache.get(failed_attempts_key, 0)
    cache.set(failed_attempts_key, failed_attempts + 1, 3600)  # Expira em 1 hora


def check_duplicate_response(ip, survey_id, time_window=300):
    """
    Verifica se há tentativa de resposta duplicada no mesmo período
    """
    cache_key = f'response_attempt:{survey_id}:{ip}'
    last_attempt = cache.get(cache_key)
    
    if last_attempt:
        time_diff = (timezone.now() - last_attempt).total_seconds()
        if time_diff < time_window:
            return True  # Tentativa duplicada
    
    cache.set(cache_key, timezone.now(), time_window)
    return False


def validate_response_content(response_data):
    """
    Valida conteúdo da resposta para detectar spam
    """
    # Verificar campos obrigatórios muito curtos (spam bots)
    for key, value in response_data.items():
        if isinstance(value, str) and len(value) < 3 and len(value) > 0:
            # Respostas muito curtas podem ser spam
            return False
    
    # Verificar palavras suspeitas (pode ser expandido)
    spam_keywords = ['http://', 'https://', 'www.', '.com', 'buy now', 'click here']
    response_text = ' '.join(str(v) for v in response_data.values()).lower()
    
    for keyword in spam_keywords:
        if keyword in response_text:
            # Pode ser spam, mas não bloquear completamente
            # Apenas marcar para revisão
            pass
    
    return True


def get_client_ip(request):
    """Obtém IP do cliente de forma segura"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_user_agent(request):
    """Verifica user agent suspeito"""
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    # User agents suspeitos (pode ser expandido)
    suspicious_agents = ['bot', 'crawler', 'spider', 'scraper']
    
    for agent in suspicious_agents:
        if agent in user_agent:
            return False
    
    return True

