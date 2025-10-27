from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('surveys/', views.surveys_list, name='surveys_list'),
    path('responses/', views.responses_list, name='responses_list'),
    path('export/csv/', views.export_responses_csv, name='export_csv'),
    path('export/excel/', views.export_responses_excel, name='export_excel'),
    path('api/nps-data/', views.api_nps_data, name='api_nps_data'),
]
