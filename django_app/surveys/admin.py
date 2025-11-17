from django.contrib import admin
from django.utils.html import format_html
from .models import Survey, Question, Choice, SurveyResponse, Answer, NPSResult, Respondent, SurveyInvitation


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    ordering = ['order']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    ordering = ['order']
    fields = ['question_text', 'question_type', 'is_required', 'order']


class SurveyInvitationInline(admin.TabularInline):
    model = SurveyInvitation
    extra = 0
    readonly_fields = ['email', 'unique_token', 'created_at', 'is_used', 'expires_at']
    can_delete = False
    fields = ['email', 'is_used', 'expires_at', 'created_at']
    show_change_link = True


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_by', 'created_at', 'response_count', 'invitation_count', 'send_invitations_link']
    list_filter = ['is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline, SurveyInvitationInline]
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Respostas'
    
    def invitation_count(self, obj):
        return obj.invitations.count()
    invitation_count.short_description = 'Convites'
    
    def send_invitations_link(self, obj):
        """Link para enviar convites e criar lista automática"""
        from django.urls import reverse
        url_send = reverse('send_survey_invitations', args=[obj.id])
        url_criar_lista = reverse('criar_lista_convidados', args=[obj.id])
        return format_html(
            '<a href="{}" class="button" style="margin-right: 5px;">Enviar Convites</a> '
            '<a href="{}" class="button" style="background-color: #28a745;">🎲 Criar Lista Automática</a>',
            url_send, url_criar_lista
        )
    send_invitations_link.short_description = 'Ações'


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


@admin.register(Respondent)
class RespondentAdmin(admin.ModelAdmin):
    list_display = ['nome_usuario', 'email', 'nome_conta', 'nome_produto', 'status_usuario', 'active', 'created_at']
    list_filter = ['status_usuario', 'active', 'created_at']
    search_fields = ['email', 'nome_usuario', 'nome_conta', 'nome_produto']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('email', 'nome_conta', 'nome_usuario', 'nome_produto', 'status_usuario', 'active')
        }),
        ('Informações Adicionais', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(SurveyInvitation)
class SurveyInvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'survey', 'status_display', 'sent_at', 'opened_at', 'clicked_at', 'created_at', 'expires_at', 'is_used', 'link_url']
    list_filter = ['is_used', 'survey', 'created_at', 'expires_at', 'sent_at', 'opened_at', 'clicked_at']
    search_fields = ['email', 'survey__title', 'unique_token']
    readonly_fields = ['unique_token', 'created_at', 'link_url', 'used_at', 'sent_at', 'opened_at', 'clicked_at', 'open_count', 'click_count']
    actions = ['resend_invitations', 'reset_expired_invitations']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações do Convite', {
            'fields': ('survey', 'email', 'unique_token', 'link_url')
        }),
        ('Status', {
            'fields': ('is_used', 'used_at', 'expires_at', 'created_at')
        }),
        ('Tracking', {
            'fields': ('sent_at', 'opened_at', 'clicked_at', 'open_count', 'click_count')
        }),
    )
    
    def status_display(self, obj):
        if obj.is_used:
            return format_html('<span style="color: green; font-weight: bold;">✓ Utilizado</span>')
        elif obj.is_expired():
            return format_html('<span style="color: red; font-weight: bold;">✗ Expirado</span>')
        else:
            return format_html('<span style="color: blue; font-weight: bold;">○ Válido</span>')
    status_display.short_description = 'Status'
    
    def link_url(self, obj):
        """Exibe o link completo do convite"""
        from django.contrib.sites.models import Site
        from django.urls import reverse
        try:
            current_site = Site.objects.get_current()
            url = f"http://{current_site.domain}/survey/{obj.survey.id}/respond/{obj.unique_token}/"
        except:
            url = f"/survey/{obj.survey.id}/respond/{obj.unique_token}/"
        return format_html('<a href="{}" target="_blank" style="font-size: 11px; word-break: break-all;">{}</a>', url, url[:50] + '...' if len(url) > 50 else url)
    link_url.short_description = 'Link do Convite'
    
    def resend_invitations(self, request, queryset):
        """Ação para reenviar convites selecionados"""
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string
        
        sent_count = 0
        failed_count = 0
        
        for invitation in queryset:
            if invitation.is_used:
                self.message_user(request, f'Convite para {invitation.email} já foi utilizado e não pode ser reenviado.', level='warning')
                failed_count += 1
                continue
            
            try:
                # Buscar respondente pelo email para obter nome_produto
                try:
                    respondent = Respondent.objects.get(email=invitation.email)
                    nome_produto = respondent.nome_produto or ''
                except Respondent.DoesNotExist:
                    nome_produto = ''
                
                # Construir URL do convite
                survey_url = request.build_absolute_uri(invitation.get_survey_url())
                
                subject = f"Convite para Pesquisa: {invitation.survey.title}"
                message = render_to_string('surveys/email_invitation.html', {
                    'survey': invitation.survey,
                    'invitation': invitation,
                    'survey_url': survey_url,
                    'expiration_date': invitation.expires_at,
                    'nome_produto': nome_produto
                })
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [invitation.email],
                    html_message=message,
                    fail_silently=False
                )
                sent_count += 1
            except Exception as e:
                self.message_user(request, f'Erro ao reenviar convite para {invitation.email}: {str(e)}', level='error')
                failed_count += 1
        
        if sent_count > 0:
            self.message_user(request, f'{sent_count} convite(s) reenviado(s) com sucesso!', level='success')
        if failed_count > 0:
            self.message_user(request, f'{failed_count} convite(s) falharam ao reenviar.', level='warning')
    resend_invitations.short_description = 'Reenviar convites selecionados por email'
    
    def reset_expired_invitations(self, request, queryset):
        """Ação para renovar convites expirados"""
        from django.utils import timezone
        from datetime import timedelta
        
        reset_count = 0
        for invitation in queryset:
            if invitation.is_expired() and not invitation.is_used:
                invitation.expires_at = timezone.now() + timedelta(days=30)
                invitation.save()
                reset_count += 1
        
        if reset_count > 0:
            self.message_user(request, f'{reset_count} convite(s) expirado(s) renovado(s) com sucesso!', level='success')
        else:
            self.message_user(request, 'Nenhum convite expirado foi encontrado para renovar.', level='info')
    reset_expired_invitations.short_description = 'Renovar convites expirados (adicionar 30 dias)'