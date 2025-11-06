@echo off
echo ============================================================
echo Solucionando Erro: No module named 'whitenoise'
echo ============================================================
echo.

REM Ir para o diretorio do script
cd /d "%~dp0"

echo Passo 1: Verificando ambiente virtual...
if not exist "venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit /b 1
)
echo OK - Ambiente virtual encontrado
echo.

echo Passo 2: Instalando whitenoise...
venv\Scripts\python.exe -m pip install whitenoise==6.6.0
echo.

echo Passo 3: Verificando instalacao...
venv\Scripts\python.exe -c "import whitenoise; print('whitenoise instalado com sucesso!')"
echo.

echo Passo 4: Entrando na pasta django_app...
cd django_app
echo.

echo Passo 5: Verificando configuracoes do Django...
..\venv\Scripts\python.exe manage.py check
echo.

echo ============================================================
echo Iniciando servidor...
echo ============================================================
echo.
echo Acesse: http://localhost:8000/admin/
echo.
echo Pressione Ctrl+C para parar
echo ============================================================
echo.

..\venv\Scripts\python.exe manage.py runserver

pause

