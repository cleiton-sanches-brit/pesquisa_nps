"""
Views para tracking de emails - abertura, cliques e comportamento
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from .models import SurveyInvitation


@csrf_exempt
def track_email_open(request, token):
    """
    Tracking de abertura de email via pixel invisível
    Retorna uma imagem 1x1 transparente
    """
    try:
        invitation = get_object_or_404(SurveyInvitation, unique_token=token)
        invitation.mark_as_opened()
    except:
        pass
    
    # Retornar pixel transparente 1x1
    pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    response = HttpResponse(pixel, content_type='image/png')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@csrf_exempt
def track_link_click(request, token):
    """
    Tracking de clique no link
    Redireciona para a página de resposta após registrar o clique
    """
    invitation = get_object_or_404(SurveyInvitation, unique_token=token)
    
    # Marcar como clicado
    invitation.mark_as_clicked()
    
    # Redirecionar para a página de resposta
    from django.shortcuts import redirect
    return redirect('respond_survey', survey_id=invitation.survey.id, token=token)


@login_required
def email_tracking_stats(request, survey_id):
    """
    API para obter estatísticas de tracking de emails
    """
    from .models import Survey
    
    survey = get_object_or_404(Survey, id=survey_id)
    invitations = survey.invitations.all()
    
    total = invitations.count()
    sent = invitations.filter(sent_at__isnull=False).count()
    opened = invitations.filter(opened_at__isnull=False).count()
    clicked = invitations.filter(clicked_at__isnull=False).count()
    responded = invitations.filter(is_used=True).count()
    
    # Categorias
    not_opened = invitations.filter(sent_at__isnull=False, opened_at__isnull=True).count()
    opened_not_clicked = invitations.filter(opened_at__isnull=False, clicked_at__isnull=True).count()
    clicked_not_responded = invitations.filter(clicked_at__isnull=False, is_used=False).count()
    
    stats = {
        'total': total,
        'sent': sent,
        'opened': opened,
        'clicked': clicked,
        'responded': responded,
        'not_opened': not_opened,
        'opened_not_clicked': opened_not_clicked,
        'clicked_not_responded': clicked_not_responded,
        'open_rate': round((opened / sent * 100) if sent > 0 else 0, 2),
        'click_rate': round((clicked / opened * 100) if opened > 0 else 0, 2),
        'response_rate': round((responded / clicked * 100) if clicked > 0 else 0, 2),
    }
    
    return JsonResponse(stats)


@login_required
def email_tracking_details(request, survey_id):
    """
    Lista detalhada de convites com status de tracking
    """
    from .models import Survey
    
    survey = get_object_or_404(Survey, id=survey_id)
    invitations = survey.invitations.all().order_by('-created_at')
    
    # Classificar por status
    categorized = {
        'not_sent': [],
        'sent_not_opened': [],
        'opened_not_clicked': [],
        'clicked_not_responded': [],
        'responded': [],
    }
    
    for invitation in invitations:
        status = invitation.get_status()
        if status == 'respondido':
            categorized['responded'].append(invitation)
        elif status == 'clicou_nao_respondeu':
            categorized['clicked_not_responded'].append(invitation)
        elif status == 'abriu_nao_clicou':
            categorized['opened_not_clicked'].append(invitation)
        elif status == 'enviado_nao_abriu':
            categorized['sent_not_opened'].append(invitation)
        else:
            categorized['not_sent'].append(invitation)
    
    context = {
        'survey': survey,
        'categorized': categorized,
        'stats': {
            'total': invitations.count(),
            'sent_not_opened': len(categorized['sent_not_opened']),
            'opened_not_clicked': len(categorized['opened_not_clicked']),
            'clicked_not_responded': len(categorized['clicked_not_responded']),
            'responded': len(categorized['responded']),
        }
    }
    
    return render(request, 'surveys/email_tracking_details.html', context)

