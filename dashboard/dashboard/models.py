from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Customer(models.Model):
    """Modelo para representar clientes"""
    name = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    company = models.CharField(max_length=200, blank=True, verbose_name="Empresa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name


class Survey(models.Model):
    """Modelo para representar pesquisas"""
    SURVEY_TYPES = [
        ('nps', 'NPS (Net Promoter Score)'),
        ('csat', 'CSAT (Customer Satisfaction)'),
        ('ces', 'CES (Customer Effort Score)'),
        ('custom', 'Personalizada'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    survey_type = models.CharField(max_length=10, choices=SURVEY_TYPES, verbose_name="Tipo")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizada em")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Criado por")
    
    class Meta:
        verbose_name = "Pesquisa"
        verbose_name_plural = "Pesquisas"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """Modelo para representar perguntas de uma pesquisa"""
    QUESTION_TYPES = [
        ('scale', 'Escala (0-10)'),
        ('text', 'Texto Livre'),
        ('choice', 'Múltipla Escolha'),
        ('rating', 'Avaliação (1-5)'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions', verbose_name="Pesquisa")
    text = models.TextField(verbose_name="Texto da Pergunta")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, verbose_name="Tipo")
    is_required = models.BooleanField(default=True, verbose_name="Obrigatória")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    
    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.survey.title} - {self.text[:50]}..."


class Response(models.Model):
    """Modelo para representar respostas de pesquisas"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='responses', verbose_name="Cliente")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses', verbose_name="Pesquisa")
    score = models.IntegerField(null=True, blank=True, verbose_name="Nota")
    comment = models.TextField(blank=True, verbose_name="Comentário")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviada em")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Endereço IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        ordering = ['-submitted_at']
        unique_together = ['customer', 'survey']
    
    def __str__(self):
        return f"{self.customer.name} - {self.survey.title} - {self.score}"
    
    @property
    def nps_category(self):
        """Categoriza a resposta NPS"""
        if self.score is None:
            return None
        if self.score >= 9:
            return 'promoter'
        elif self.score >= 7:
            return 'passive'
        else:
            return 'detractor'


class SurveySummary(models.Model):
    """Modelo para armazenar resumos calculados de pesquisas"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='summaries', verbose_name="Pesquisa")
    period_start = models.DateField(verbose_name="Início do Período")
    period_end = models.DateField(verbose_name="Fim do Período")
    total_responses = models.PositiveIntegerField(verbose_name="Total de Respostas")
    average_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nota Média")
    promoters = models.PositiveIntegerField(verbose_name="Promotores")
    passives = models.PositiveIntegerField(verbose_name="Neutros")
    detractors = models.PositiveIntegerField(verbose_name="Detratores")
    nps_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score NPS")
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="Calculado em")
    
    class Meta:
        verbose_name = "Resumo da Pesquisa"
        verbose_name_plural = "Resumos das Pesquisas"
        ordering = ['-calculated_at']
        unique_together = ['survey', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.survey.title} - {self.period_start} a {self.period_end} - NPS: {self.nps_score}"