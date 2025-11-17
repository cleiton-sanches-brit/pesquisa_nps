"""
URLs para funcionalidades de NPS
"""
from django.urls import path
from . import views_nps

urlpatterns = [
    # Dashboard NPS
    path('nps/dashboard/', views_nps.nps_dashboard, name='nps_dashboard'),
    path('nps/dashboard/<int:survey_id>/', views_nps.nps_dashboard, name='nps_dashboard_survey'),
    
    # API de dados NPS
    path('nps/api/<int:survey_id>/data/', views_nps.nps_api_data, name='nps_api_data'),
    
    # Calcular NPS
    path('nps/calculate/<int:survey_id>/', views_nps.nps_calculate, name='nps_calculate'),
    
    # Exportação
    path('nps/export/<int:survey_id>/excel/', views_nps.export_nps_excel, name='export_nps_excel'),
    path('nps/export/<int:survey_id>/csv/', views_nps.export_nps_csv, name='export_nps_csv'),
]

