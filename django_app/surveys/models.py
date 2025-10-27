from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Survey(models.Model):
    """Modelo para representar uma pesquisa NPS"""
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
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
    """Modelo para representar as perguntas de uma pesquisa"""
    QUESTION_TYPES = [
        ('nps', 'NPS (0-10)'),
        ('text', 'Texto Livre'),
        ('choice', 'Múltipla Escolha'),
        ('rating', 'Avaliação (1-5)'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions', verbose_name="Pesquisa")
    question_text = models.TextField(verbose_name="Texto da Pergunta")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, verbose_name="Tipo")
    is_required = models.BooleanField(default=True, verbose_name="Obrigatória")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    
    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.survey.title} - {self.question_text[:50]}..."


class Choice(models.Model):
    """Modelo para opções de múltipla escolha"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="Pergunta")
    choice_text = models.CharField(max_length=200, verbose_name="Texto da Opção")
    value = models.CharField(max_length=50, verbose_name="Valor")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    class Meta:
        verbose_name = "Opção"
        verbose_name_plural = "Opções"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.choice_text}"


class SurveyResponse(models.Model):
    """Modelo para representar uma resposta completa de pesquisa"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses', verbose_name="Pesquisa")
    respondent_id = models.CharField(max_length=100, verbose_name="ID do Respondente")
    respondent_email = models.EmailField(blank=True, verbose_name="Email do Respondente")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviada em")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Endereço IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    class Meta:
        verbose_name = "Resposta da Pesquisa"
        verbose_name_plural = "Respostas das Pesquisas"
        ordering = ['-submitted_at']
        unique_together = ['survey', 'respondent_id']
    
    def __str__(self):
        return f"{self.survey.title} - {self.respondent_id}"


class Answer(models.Model):
    """Modelo para representar uma resposta individual a uma pergunta"""
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers', verbose_name="Resposta")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Pergunta")
    answer_text = models.TextField(blank=True, verbose_name="Resposta em Texto")
    answer_value = models.CharField(max_length=100, blank=True, verbose_name="Valor da Resposta")
    answer_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Opção Escolhida")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")
    
    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        unique_together = ['response', 'question']
    
    def __str__(self):
        return f"{self.response.respondent_id} - {self.question.question_text[:30]}..."


class NPSResult(models.Model):
    """Modelo para armazenar resultados calculados de NPS"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='nps_results', verbose_name="Pesquisa")
    period_start = models.DateField(verbose_name="Início do Período")
    period_end = models.DateField(verbose_name="Fim do Período")
    total_responses = models.PositiveIntegerField(verbose_name="Total de Respostas")
    promoters = models.PositiveIntegerField(verbose_name="Promotores (9-10)")
    passives = models.PositiveIntegerField(verbose_name="Neutros (7-8)")
    detractors = models.PositiveIntegerField(verbose_name="Detratores (0-6)")
    nps_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score NPS")
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="Calculado em")
    
    class Meta:
        verbose_name = "Resultado NPS"
        verbose_name_plural = "Resultados NPS"
        ordering = ['-calculated_at']
        unique_together = ['survey', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.survey.title} - {self.period_start} a {self.period_end} - NPS: {self.nps_score}"