from django.contrib import admin
from django.utils.html import format_html
from .models import Survey, Question, Choice, SurveyResponse, Answer, NPSResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    ordering = ['order']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    ordering = ['order']
    fields = ['question_text', 'question_type', 'is_required', 'order']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_by', 'created_at', 'response_count']
    list_filter = ['is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Respostas'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'survey', 'question_type', 'is_required', 'order']
    list_filter = ['question_type', 'is_required', 'survey']
    search_fields = ['question_text', 'survey__title']
    ordering = ['survey', 'order']
    inlines = [ChoiceInline]
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Pergunta'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'value', 'order']
    list_filter = ['question__survey']
    search_fields = ['choice_text', 'question__question_text']
    ordering = ['question', 'order']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question', 'answer_text', 'answer_value', 'answer_choice', 'created_at']
    can_delete = False


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['respondent_id', 'survey', 'respondent_email', 'submitted_at', 'answer_count']
    list_filter = ['survey', 'submitted_at']
    search_fields = ['respondent_id', 'respondent_email', 'survey__title']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent']
    inlines = [AnswerInline]
    
    def answer_count(self, obj):
        return obj.answers.count()
    answer_count.short_description = 'Respostas'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['response', 'question_short', 'answer_display', 'created_at']
    list_filter = ['question__survey', 'question__question_type', 'created_at']
    search_fields = ['response__respondent_id', 'question__question_text']
    readonly_fields = ['created_at']
    
    def question_short(self, obj):
        return obj.question.question_text[:50] + '...' if len(obj.question.question_text) > 50 else obj.question.question_text
    question_short.short_description = 'Pergunta'
    
    def answer_display(self, obj):
        if obj.answer_text:
            return obj.answer_text[:50] + '...' if len(obj.answer_text) > 50 else obj.answer_text
        elif obj.answer_value:
            return obj.answer_value
        elif obj.answer_choice:
            return obj.answer_choice.choice_text
        return '-'
    answer_display.short_description = 'Resposta'


@admin.register(NPSResult)
class NPSResultAdmin(admin.ModelAdmin):
    list_display = ['survey', 'period_start', 'period_end', 'total_responses', 'nps_score_display', 'calculated_at']
    list_filter = ['survey', 'calculated_at']
    search_fields = ['survey__title']
    readonly_fields = ['calculated_at', 'nps_score']
    
    def nps_score_display(self, obj):
        color = 'green' if obj.nps_score >= 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.nps_score
        )
    nps_score_display.short_description = 'Score NPS'