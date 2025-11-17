@echo off
echo ============================================
echo Executando Testes do Sistema NPS Surveys
echo ============================================
echo.

cd django_app
..\venv\Scripts\python.exe manage.py test surveys --verbosity=2

pause

