from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Survey, Question, SurveyResponse, Answer, NPSResult
from .serializers import (
    SurveySerializer, SurveyResponseSerializer, 
    SurveyResponseListSerializer, NPSResultSerializer
)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Survey.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset
    
    @action(detail=True, methods=['get'])
    def responses(self, request, pk=None):
        """Lista todas as respostas de uma pesquisa específica"""
        survey = self.get_object()
        responses = survey.responses.all()
        serializer = SurveyResponseListSerializer(responses, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def nps_results(self, request, pk=None):
        """Lista os resultados NPS de uma pesquisa específica"""
        survey = self.get_object()
        results = survey.nps_results.all()
        serializer = NPSResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def calculate_nps(self, request, pk=None):
        """Calcula o NPS para um período específico"""
        survey = self.get_object()
        
        # Obter parâmetros do request
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')
        
        if not period_start or not period_end:
            return Response(
                {'error': 'period_start e period_end são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = datetime.strptime(period_start, '%Y-%m-%d').date()
            end_date = datetime.strptime(period_end, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Formato de data inválido. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se já existe resultado para este período
        existing_result = NPSResult.objects.filter(
            survey=survey,
            period_start=start_date,
            period_end=end_date
        ).first()
        
        if existing_result:
            return Response(
                {'error': 'Resultado NPS já existe para este período'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar respostas do período
        responses = survey.responses.filter(
            submitted_at__date__range=[start_date, end_date]
        )
        
        # Buscar perguntas NPS
        nps_questions = survey.questions.filter(question_type='nps')
        
        if not nps_questions.exists():
            return Response(
                {'error': 'Nenhuma pergunta NPS encontrada nesta pesquisa'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular NPS
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
                    except ValueError:
                        continue
        
        if total_responses == 0:
            return Response(
                {'error': 'Nenhuma resposta NPS encontrada para este período'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular score NPS
        nps_score = ((promoters - detractors) / total_responses) * 100
        
        # Criar resultado NPS
        nps_result = NPSResult.objects.create(
            survey=survey,
            period_start=start_date,
            period_end=end_date,
            total_responses=total_responses,
            promoters=promoters,
            passives=passives,
            detractors=detractors,
            nps_score=nps_score
        )
        
        serializer = NPSResultSerializer(nps_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = []  # Permitir acesso público para envio de respostas
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SurveyResponseListSerializer
        return SurveyResponseSerializer
    
    def get_queryset(self):
        queryset = SurveyResponse.objects.all()
        survey_id = self.request.query_params.get('survey')
        if survey_id:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Criar nova resposta de pesquisa (endpoint público)"""
        # Adicionar informações do request
        request.data['ip_address'] = self.get_client_ip(request)
        request.data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        return super().create(request, *args, **kwargs)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip