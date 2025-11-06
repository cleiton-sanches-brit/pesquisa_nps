@echo off
echo Iniciando Projeto NPS Surveys...
echo ================================

REM Navegar para o diretorio correto
cd /d "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps"

REM Parar processos Python existentes
taskkill /f /im python.exe 2>nul

echo.
echo Iniciando Django...
start "Django Server" cmd /k "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\venv\Scripts\python.exe django_app\manage.py runserver 0.0.0.0:8000"

echo Aguardando Django inicializar...
timeout /t 10 /nobreak >nul

echo.
echo Iniciando FastAPI...
start "FastAPI Server" cmd /k "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001"

echo.
echo ================================
echo Servicos iniciados!
echo.
echo Django Admin: http://localhost:8000/admin/
echo FastAPI Docs: http://localhost:8001/docs
echo Login: admin / admin123
echo.
echo Pressione qualquer tecla para parar os servicos...
pause >nul

echo.
echo Parando servicos...
taskkill /f /im python.exe 2>nul
echo Servicos parados!
pause

