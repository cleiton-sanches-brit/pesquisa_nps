from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'responses', views.SurveyResponseViewSet)

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    # URLs de convites e respostas
    path('', include('surveys.urls_invitations')),
    # URLs de NPS (dashboard e exportação)
    path('', include('surveys.urls_nps')),
    # URLs de tracking de emails
    path('', include('surveys.urls_tracking')),
]
