"""
Middleware para segurança - rate limiting e proteção contra spam
"""
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
import hashlib
import json


class RateLimitMiddleware:
    """
    Middleware para rate limiting baseado em IP
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Limites por tipo de endpoint
        self.rate_limits = {
            'survey_response': {
                'limit': 5,  # 5 respostas por hora
                'window': 3600,  # 1 hora
            },
            'survey_invitation': {
                'limit': 10,  # 10 convites por hora
                'window': 3600,
            },
            'api': {
                'limit': 100,  # 100 requests por hora
                'window': 3600,
            },
            'tracking': {
                'limit': 1000,  # 1000 requests por hora (tracking pixel)
                'window': 3600,
            },
        }
    
    def __call__(self, request):
        # Verificar rate limit apenas para métodos que modificam dados
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            endpoint_type = self._get_endpoint_type(request.path)
            if endpoint_type:
                if not self._check_rate_limit(request, endpoint_type):
                    return JsonResponse({
                        'error': 'Muitas requisições. Por favor, tente novamente mais tarde.',
                        'retry_after': self._get_retry_after(request, endpoint_type)
                    }, status=429)
        
        response = self.get_response(request)
        return response
    
    def _get_endpoint_type(self, path):
        """Identifica o tipo de endpoint para aplicar rate limit"""
        if '/survey/' in path and '/respond/' in path:
            return 'survey_response'
        elif '/invite/' in path or '/invitation/' in path:
            return 'survey_invitation'
        elif '/api/' in path:
            return 'api'
        elif '/track/' in path:
            return 'tracking'
        return None
    
    def _get_client_ip(self, request):
        """Obtém o IP do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_cache_key(self, ip, endpoint_type):
        """Gera chave de cache para rate limiting"""
        return f'ratelimit:{endpoint_type}:{ip}'
    
    def _check_rate_limit(self, request, endpoint_type):
        """Verifica se o limite foi excedido"""
        ip = self._get_client_ip(request)
        limit_config = self.rate_limits.get(endpoint_type)
        
        if not limit_config:
            return True
        
        cache_key = self._get_cache_key(ip, endpoint_type)
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit_config['limit']:
            return False
        
        # Incrementar contador
        cache.set(cache_key, current_count + 1, limit_config['window'])
        return True
    
    def _get_retry_after(self, request, endpoint_type):
        """Retorna tempo em segundos até poder tentar novamente"""
        limit_config = self.rate_limits.get(endpoint_type)
        if limit_config:
            return limit_config['window']
        return 3600


class SpamProtectionMiddleware:
    """
    Middleware para proteção contra spam
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar apenas para POST de respostas
        if request.method == 'POST' and '/survey/' in request.path and '/respond/' in request.path:
            if self._is_spam(request):
                return JsonResponse({
                    'error': 'Sua requisição foi identificada como spam. Por favor, tente novamente.',
                }, status=403)
        
        response = self.get_response(request)
        return response
    
    def _is_spam(self, request):
        """Verifica se a requisição é spam"""
        # Verificar honeypot field (campo que deve estar vazio)
        honeypot = request.POST.get('website', '') or request.POST.get('url', '')
        if honeypot:
            return True
        
        # Verificar tempo mínimo entre requisições (velocidade de preenchimento)
        ip = self._get_client_ip(request)
        cache_key = f'spam_check:{ip}'
        last_request = cache.get(cache_key)
        
        if last_request:
            # Se preencheu muito rápido (menos de 5 segundos), pode ser spam
            time_diff = (timezone.now() - last_request).total_seconds()
            if time_diff < 5:
                return True
        
        # Registrar timestamp da requisição
        cache.set(cache_key, timezone.now(), 60)  # Cache por 1 minuto
        
        return False
    
    def _get_client_ip(self, request):
        """Obtém o IP do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

