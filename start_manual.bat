@echo off
echo ========================================
echo    PROJETO NPS SURVEYS - INICIANDO
echo ========================================
echo.

REM Navegar para o diretorio correto
cd /d "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps"

REM Parar processos Python existentes
echo Parando processos Python existentes...
taskkill /f /im python.exe 2>nul

echo.
echo Iniciando Django na porta 8000...
echo (Abra uma nova janela de comando para ver os logs)
start "Django Server" cmd /c "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\venv\Scripts\python.exe django_app\manage.py runserver 0.0.0.0:8000 & pause"

echo.
echo Iniciando FastAPI na porta 8001...
echo (Abra uma nova janela de comando para ver os logs)
start "FastAPI Server" cmd /c "C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 & pause"

echo.
echo ========================================
echo    SERVICOS INICIADOS COM SUCESSO!
echo ========================================
echo.
echo Acesse as seguintes URLs:
echo.
echo Django Admin: http://localhost:8000/admin/
echo   - Login: admin
echo   - Senha: admin123
echo.
echo FastAPI Docs: http://localhost:8001/docs
echo   - Documentacao interativa da API
echo.
echo ========================================
echo.
echo Pressione qualquer tecla para parar os servicos...
pause >nul

echo.
echo Parando servicos...
taskkill /f /im python.exe 2>nul
echo Servicos parados!
echo.
pause

