from rest_framework import serializers
from .models import Survey, Question, Choice, SurveyResponse, Answer, NPSResult


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'value', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'is_required', 'order', 'choices']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    response_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at', 'created_by', 'questions', 'response_count']
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_response_count(self, obj):
        return obj.responses.count()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text', 'answer_value', 'answer_choice']


class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    
    class Meta:
        model = SurveyResponse
        fields = ['survey', 'respondent_id', 'respondent_email', 'answers']
    
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        response = SurveyResponse.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(response=response, **answer_data)
        
        return response


class NPSResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPSResult
        fields = ['id', 'survey', 'period_start', 'period_end', 'total_responses', 
                 'promoters', 'passives', 'detractors', 'nps_score', 'calculated_at']
        read_only_fields = ['calculated_at', 'nps_score']


class SurveyResponseListSerializer(serializers.ModelSerializer):
    survey_title = serializers.CharField(source='survey.title', read_only=True)
    answer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SurveyResponse
        fields = ['id', 'respondent_id', 'respondent_email', 'survey_title', 'submitted_at', 'answer_count']
    
    def get_answer_count(self, obj):
        return obj.answers.count()
