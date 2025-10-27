from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Survey, Question, Response, SurveySummary


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'created_at', 'response_count']
    list_filter = ['created_at', 'company']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Respostas'


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'survey_type', 'is_active', 'created_by', 'created_at', 'response_count']
    list_filter = ['survey_type', 'is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Respostas'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'survey', 'question_type', 'is_required', 'order']
    list_filter = ['question_type', 'is_required', 'survey__survey_type']
    search_fields = ['text', 'survey__title']
    ordering = ['survey', 'order']
    
    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Pergunta'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['customer', 'survey', 'score', 'nps_category_display', 'submitted_at']
    list_filter = ['survey__survey_type', 'submitted_at', 'score']
    search_fields = ['customer__name', 'customer__email', 'survey__title']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent']
    
    def nps_category_display(self, obj):
        category = obj.nps_category
        if category == 'promoter':
            return format_html('<span style="color: green; font-weight: bold;">Promotor</span>')
        elif category == 'passive':
            return format_html('<span style="color: orange; font-weight: bold;">Neutro</span>')
        elif category == 'detractor':
            return format_html('<span style="color: red; font-weight: bold;">Detrator</span>')
        return '-'
    nps_category_display.short_description = 'Categoria NPS'


@admin.register(SurveySummary)
class SurveySummaryAdmin(admin.ModelAdmin):
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