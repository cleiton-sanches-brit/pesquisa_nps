from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'responses', views.SurveyResponseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
