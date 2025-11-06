"""
URLs para tracking de emails
"""
from django.urls import path
from . import views_tracking

urlpatterns = [
    # Tracking de email
    path('track/email/open/<uuid:token>/', views_tracking.track_email_open, name='track_email_open'),
    path('track/link/click/<uuid:token>/', views_tracking.track_link_click, name='track_link_click'),
    
    # Estatísticas e detalhes
    path('survey/<int:survey_id>/tracking/', views_tracking.email_tracking_details, name='email_tracking_details'),
    path('survey/<int:survey_id>/tracking/stats/', views_tracking.email_tracking_stats, name='email_tracking_stats'),
]

