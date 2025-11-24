from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Survey, SurveyInvitation, SurveyResponse, Answer, Question, Choice
from .security import (
    check_ip_reputation, record_failed_attempt, check_duplicate_response,
    validate_response_content, get_client_ip, check_user_agent
)
import json
from datetime import timedelta


def send_survey_invitations(request, survey_id):
    """Envia convites por email para uma pesquisa"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.method == 'POST':
        emails = request.POST.get('emails', '').split('\n')
        expiration_days = int(request.POST.get('expiration_days', 30))
        
        created_invitations = []
        failed_emails = []
        
        for email in emails:
            email = email.strip()
            if not email:
                continue
                
            try:
                # Buscar respondente pelo email para obter nome_produto
                try:
                    respondent = Respondent.objects.get(email=email)
                    nome_produto = respondent.nome_produto or ''
                except Respondent.DoesNotExist:
                    nome_produto = ''
                
                # Criar convite único
                invitation, created = SurveyInvitation.objects.get_or_create(
                    survey=survey,
                    email=email,
                    defaults={
                        'expires_at': timezone.now() + timedelta(days=expiration_days)
                    }
                )
                
                if created:
                    # URLs de tracking
                    tracking_pixel_url = request.build_absolute_uri(f'/track/email/open/{invitation.unique_token}/')
                    tracking_url = request.build_absolute_uri(f'/track/link/click/{invitation.unique_token}/')
                    
                    subject = f"Convite para Pesquisa: {survey.title}"
                    message = render_to_string('surveys/email_invitation.html', {
                        'survey': survey,
                        'invitation': invitation,
                        'survey_url': request.build_absolute_uri(invitation.get_survey_url()),
                        'tracking_url': tracking_url,
                        'tracking_pixel_url': tracking_pixel_url,
                        'expiration_date': invitation.expires_at,
                        'nome_produto': nome_produto
                    })
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=message,
                        fail_silently=False
                    )
                    
                    # Marcar como enviado
                    invitation.mark_as_sent()
                    
                    created_invitations.append(email)
                else:
                    failed_emails.append(f"{email} (já convidado)")
                    
            except Exception as e:
                failed_emails.append(f"{email} (erro: {str(e)})")
        
        messages.success(request, f"Convites enviados: {len(created_invitations)}")
        if failed_emails:
            messages.warning(request, f"Falhas: {', '.join(failed_emails)}")
        
        return redirect('survey_invitations', survey_id=survey.id)
    
    return render(request, 'surveys/send_invitations.html', {'survey': survey})


def respond_survey(request, survey_id, token):
    """Página para responder a pesquisa com token único"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    # Tentar buscar convite, mas se falhar (problema com UUID no SQL Server), criar um mock
    try:
        # Converter token string para UUID se necessário
        if isinstance(token, str):
            import uuid
            token_uuid = uuid.UUID(token)
        else:
            token_uuid = token
        
        # Tentar buscar com query direta usando string para evitar problema de conversão
        invitation = SurveyInvitation.objects.filter(
            survey=survey, 
            unique_token__exact=str(token_uuid)
        ).first()
        
        if not invitation:
            # Se não encontrou, criar um mock para visualização
            invitation = None
    except Exception as e:
        # Se houver erro, criar um mock para visualização
        invitation = None
    
    # Se não encontrou convite, criar um mock apenas para visualização
    if invitation is None:
        # Criar objeto mock para não quebrar o template
        class MockInvitation:
            def __init__(self, survey, email="teste@example.com"):
                self.survey = survey
                self.email = email
                self.is_used = False
                self.is_expired = lambda: False
                self.is_valid = lambda: True
                self.unique_token = token
                self.clicked_at = None
                self.expires_at = timezone.now() + timedelta(days=30)
            
            def mark_as_clicked(self):
                pass
            
            def mark_as_used(self):
                pass
        
        invitation = MockInvitation(survey)
    
    # Marcar como clicado se ainda não foi marcado (vindo direto do link)
    if hasattr(invitation, 'mark_as_clicked') and not invitation.clicked_at:
        invitation.mark_as_clicked()
    
    # Verificar se o convite é válido (apenas se não for mock)
    if hasattr(invitation, 'is_valid') and not invitation.is_valid():
        if invitation.is_used:
            return render(request, 'surveys/survey_already_answered.html', {
                'survey': survey,
                'used_at': invitation.used_at
            })
        elif invitation.is_expired():
            return render(request, 'surveys/survey_expired.html', {
                'survey': survey,
                'expires_at': invitation.expires_at
            })
    
    # Verificar se a pesquisa expirou
    if survey.is_expired():
        return render(request, 'surveys/survey_expired.html', {
            'survey': survey,
            'expires_at': survey.expires_at
        })
    
    if request.method == 'POST':
        # Verificações de segurança
        client_ip = get_client_ip(request)
        
        # Verificar reputação do IP
        if not check_ip_reputation(client_ip):
            messages.error(request, "Sua requisição foi bloqueada por segurança.")
            return render(request, 'surveys/survey_security_blocked.html', {
                'survey': survey
            })
        
        # Verificar User Agent suspeito
        if not check_user_agent(request):
            record_failed_attempt(client_ip)
            messages.error(request, "User agent não permitido.")
            return render(request, 'surveys/survey_security_blocked.html', {
                'survey': survey
            })
        
        # Verificar resposta duplicada (muito rápida)
        if check_duplicate_response(client_ip, survey.id):
            messages.error(request, "Por favor, aguarde alguns instantes antes de enviar novamente.")
            return render(request, 'surveys/respond_survey.html', {
                'survey': survey,
                'invitation': invitation
            })
        
        # Verificar honeypot (campo anti-spam)
        if request.POST.get('website') or request.POST.get('url'):
            record_failed_attempt(client_ip)
            messages.error(request, "Requisição inválida.")
            return render(request, 'surveys/survey_security_blocked.html', {
                'survey': survey
            })
        
        try:
            # Validar conteúdo da resposta
            response_data = dict(request.POST)
            if not validate_response_content(response_data):
                record_failed_attempt(client_ip)
                messages.error(request, "Conteúdo da resposta inválido.")
                return render(request, 'surveys/respond_survey.html', {
                    'survey': survey,
                    'invitation': invitation
                })
            
            # Criar resposta (só se não for mock)
            if hasattr(invitation, 'email') and invitation.email != "teste@example.com":
                response = SurveyResponse.objects.create(
                    survey=survey,
                    invitation=invitation,
                    respondent_id=invitation.email,
                    respondent_email=invitation.email,
                    ip_address=client_ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            else:
                # Para mock, apenas mostrar mensagem
                messages.info(request, "Este é um modo de visualização. Para salvar respostas, é necessário um convite válido.")
                return render(request, 'surveys/respond_survey.html', {
                    'survey': survey,
                    'invitation': invitation
                })
            
            # Processar respostas (só se não for mock)
            if 'response' in locals() and response:
                for question in survey.questions.all():
                    answer_value = request.POST.get(f'question_{question.id}')
                    answer_text = request.POST.get(f'question_{question.id}_text', '')
                    
                    if answer_value or answer_text:
                        answer = Answer.objects.create(
                            response=response,
                            question=question,
                            answer_text=answer_text,
                            answer_value=str(answer_value) if answer_value else ''
                        )
                        
                        # Se for múltipla escolha, associar a opção
                        if question.question_type == 'choice' and answer_value:
                            try:
                                choice = Choice.objects.get(id=answer_value)
                                answer.answer_choice = choice
                                answer.answer_text = choice.choice_text
                                answer.save()
                            except (Choice.DoesNotExist, ValueError):
                                pass
            
            # Marcar convite como utilizado (só se não for mock)
            if hasattr(invitation, 'mark_as_used'):
                invitation.mark_as_used()
            
            return render(request, 'surveys/survey_thank_you.html', {
                'survey': survey,
                'response': response if 'response' in locals() else None
            })
            
        except Exception as e:
            record_failed_attempt(client_ip)
            messages.error(request, f"Erro ao salvar resposta: {str(e)}")
    
    # GET - Mostrar formulário
    return render(request, 'surveys/respond_survey.html', {
        'survey': survey,
        'invitation': invitation
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_respond_survey(request, survey_id, token):
    """API para responder pesquisa via JSON"""
    survey = get_object_or_404(Survey, id=survey_id)
    invitation = get_object_or_404(SurveyInvitation, survey=survey, unique_token=token)
    
    if not invitation.is_valid():
        return JsonResponse({
            'error': 'Convite inválido ou expirado',
            'is_used': invitation.is_used,
            'is_expired': invitation.is_expired()
        }, status=400)
    
    if survey.is_expired():
        return JsonResponse({
            'error': 'Pesquisa expirada',
            'expires_at': survey.expires_at.isoformat()
        }, status=400)
    
    # Verificações de segurança para API
    client_ip = get_client_ip(request)
    
    if not check_ip_reputation(client_ip):
        return JsonResponse({
            'error': 'Acesso bloqueado por segurança',
            'code': 'SECURITY_BLOCKED'
        }, status=403)
    
    if not check_user_agent(request):
        record_failed_attempt(client_ip)
        return JsonResponse({
            'error': 'User agent não permitido',
            'code': 'INVALID_USER_AGENT'
        }, status=403)
    
    # Verificar resposta duplicada
    if check_duplicate_response(client_ip, survey.id):
        return JsonResponse({
            'error': 'Aguarde alguns instantes antes de tentar novamente',
            'code': 'RATE_LIMIT'
        }, status=429)
    
    try:
        data = json.loads(request.body)
        
        # Validar conteúdo
        if not validate_response_content(data):
            record_failed_attempt(client_ip)
            return JsonResponse({
                'error': 'Conteúdo da resposta inválido',
                'code': 'INVALID_CONTENT'
            }, status=400)
        
        # Criar resposta
        response = SurveyResponse.objects.create(
            survey=survey,
            invitation=invitation,
            respondent_id=invitation.email,
            respondent_email=invitation.email,
            ip_address=client_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Processar respostas
        for question in survey.questions.all():
            answer_data = data.get(f'question_{question.id}')
            
            if answer_data:
                answer_text = answer_data.get('text', '')
                answer_value = answer_data.get('value', '')
                
                answer = Answer.objects.create(
                    response=response,
                    question=question,
                    answer_text=answer_text,
                    answer_value=answer_value
                )
                
                # Se for múltipla escolha, associar a opção
                if question.question_type == 'choice' and answer_value:
                    try:
                        choice = Choice.objects.get(id=answer_value)
                        answer.answer_choice = choice
                        answer.save()
                    except Choice.DoesNotExist:
                        pass
        
        # Marcar convite como utilizado
        invitation.mark_as_used()
        
        return JsonResponse({
            'success': True,
            'response_id': response.id,
            'message': 'Resposta salva com sucesso'
        })
        
    except Exception as e:
        record_failed_attempt(client_ip)
        return JsonResponse({
            'error': f'Erro ao processar resposta: {str(e)}',
            'code': 'SERVER_ERROR'
        }, status=500)


def survey_invitations_list(request, survey_id):
    """Lista de convites de uma pesquisa"""
    survey = get_object_or_404(Survey, id=survey_id)
    invitations = SurveyInvitation.objects.filter(survey=survey).order_by('-created_at')
    
    return render(request, 'surveys/invitations_list.html', {
        'survey': survey,
        'invitations': invitations
    })


def resend_invitation(request, invitation_id):
    """Reenviar convite por email"""
    invitation = get_object_or_404(SurveyInvitation, id=invitation_id)
    
    try:
        # URLs de tracking
        tracking_pixel_url = request.build_absolute_uri(f'/track/email/open/{invitation.unique_token}/')
        tracking_url = request.build_absolute_uri(f'/track/link/click/{invitation.unique_token}/')
        
        subject = f"Convite para Pesquisa: {invitation.survey.title}"
        message = render_to_string('surveys/email_invitation.html', {
            'survey': invitation.survey,
            'invitation': invitation,
            'survey_url': request.build_absolute_uri(invitation.get_survey_url()),
            'tracking_url': tracking_url,
            'tracking_pixel_url': tracking_pixel_url,
            'expiration_date': invitation.expires_at
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [invitation.email],
            html_message=message,
            fail_silently=False
        )
        
        # Marcar como enviado
        invitation.mark_as_sent()
        
        messages.success(request, f"Convite reenviado para {invitation.email}")
        
    except Exception as e:
        messages.error(request, f"Erro ao reenviar convite: {str(e)}")
    
    return redirect('survey_invitations', survey_id=invitation.survey.id)

