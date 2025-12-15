@echo off
echo ================================================================================
echo    INICIANDO SERVIDOR DJANGO - Sistema de Pesquisas NPS
echo ================================================================================
echo.

REM Navegar para a pasta do Django
cd /d "%~dp0django_app"
if errorlevel 1 (
    echo ERRO: Nao foi possivel encontrar a pasta django_app
    pause
    exit /b 1
)

REM Configurar SQLite para desenvolvimento local
set USE_SQLITE=true

REM Verificar se o ambiente virtual existe
if exist "..\pesquisas_nps\venv\Scripts\python.exe" (
    echo Usando ambiente virtual...
    echo.
    echo ================================================================================
    echo Servidor iniciando em http://localhost:8000
    echo Acesse: http://localhost:8000/admin/
    echo Usuario: admin | Senha: admin123
    echo.
    echo Pressione CTRL+C para parar o servidor
    echo ================================================================================
    echo.
    "..\pesquisas_nps\venv\Scripts\python.exe" manage.py runserver
) else if exist "..\..\pesquisas_nps\venv\Scripts\python.exe" (
    echo Usando ambiente virtual...
    echo.
    echo ================================================================================
    echo Servidor iniciando em http://localhost:8000
    echo Acesse: http://localhost:8000/admin/
    echo Usuario: admin | Senha: admin123
    echo.
    echo Pressione CTRL+C para parar o servidor
    echo ================================================================================
    echo.
    "..\..\pesquisas_nps\venv\Scripts\python.exe" manage.py runserver
) else (
    echo Usando Python do sistema...
    echo.
    echo ================================================================================
    echo Servidor iniciando em http://localhost:8000
    echo Acesse: http://localhost:8000/admin/
    echo Usuario: admin | Senha: admin123
    echo.
    echo Pressione CTRL+C para parar o servidor
    echo ================================================================================
    echo.
    python manage.py runserver
)

pause

