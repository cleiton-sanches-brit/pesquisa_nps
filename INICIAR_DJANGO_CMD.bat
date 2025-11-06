@echo off
echo ============================================================
echo Iniciando servidor Django
echo ============================================================
echo.

REM Ir para o diretorio do script
cd /d "%~dp0"

REM Verificar se estamos no lugar certo
if not exist "django_app\manage.py" (
    echo ERRO: Arquivo manage.py nao encontrado!
    echo Certifique-se de executar este arquivo da raiz do projeto.
    pause
    exit /b 1
)

echo Entrando na pasta django_app...
cd django_app
echo.

REM Verificar Python do venv
if exist "..\venv\Scripts\python.exe" (
    set PYTHON_CMD=..\venv\Scripts\python.exe
    echo Python encontrado: %PYTHON_CMD%
) else if exist "..\..\venv\Scripts\python.exe" (
    set PYTHON_CMD=..\..\venv\Scripts\python.exe
    echo Python encontrado: %PYTHON_CMD%
) else (
    echo AVISO: Python do venv nao encontrado, tentando Python do sistema...
    set PYTHON_CMD=python
)

echo.
echo ============================================================
echo Iniciando servidor na porta 8000...
echo ============================================================
echo.
echo Acesse: http://localhost:8000
echo Admin: http://localhost:8000/admin/
echo.
echo Pressione Ctrl+C para parar o servidor
echo ============================================================
echo.

%PYTHON_CMD% manage.py runserver

pause
