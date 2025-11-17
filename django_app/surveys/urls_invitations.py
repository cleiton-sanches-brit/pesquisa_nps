from django.urls import path
from . import views_invitations, views_selecao

urlpatterns = [
    # Convites e respostas
    path('survey/<int:survey_id>/invite/', views_invitations.send_survey_invitations, name='send_survey_invitations'),
    path('survey/<int:survey_id>/respond/<uuid:token>/', views_invitations.respond_survey, name='respond_survey'),
    path('survey/<int:survey_id>/invitations/', views_invitations.survey_invitations_list, name='survey_invitations'),
    path('invitation/<int:invitation_id>/resend/', views_invitations.resend_invitation, name='resend_invitation'),
    
    # Seleção automática de convidados
    path('survey/<int:survey_id>/criar-lista-convidados/', views_selecao.criar_lista_convidados, name='criar_lista_convidados'),
    path('survey/<int:survey_id>/preview-selecao/', views_selecao.preview_selecao_convidados, name='preview_selecao_convidados'),
    
    # API para respostas
    path('api/survey/<int:survey_id>/respond/<uuid:token>/', views_invitations.api_respond_survey, name='api_respond_survey'),
]

