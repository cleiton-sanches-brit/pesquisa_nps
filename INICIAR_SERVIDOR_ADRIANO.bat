@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================================================================
echo    INICIANDO SERVIDOR DJANGO - Sistema de Pesquisas NPS
echo    Configuracao para Adriano
echo ================================================================================
echo.

REM Salvar o diretório atual
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%"

REM Navegar para a pasta do Django
echo [1/5] Navegando para a pasta django_app...
cd /d "%SCRIPT_DIR%django_app"
if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel encontrar a pasta django_app
    echo Caminho esperado: %SCRIPT_DIR%django_app
    echo.
    pause
    exit /b 1
)
echo OK - Pasta django_app encontrada
echo.

REM Verificar se manage.py existe
echo [2/5] Verificando arquivo manage.py...
if not exist "manage.py" (
    echo.
    echo ERRO: Arquivo manage.py nao encontrado!
    echo Diretorio atual: %CD%
    echo.
    pause
    exit /b 1
)
echo OK - manage.py encontrado
echo.

REM Configurar SQLite para desenvolvimento local
echo [3/5] Configurando variaveis de ambiente...
set USE_SQLITE=true
set DEBUG=True
set ALLOWED_HOSTS=localhost,127.0.0.1
echo OK - USE_SQLITE=true configurado
echo.

REM Verificar Python
echo [4/5] Verificando Python...
set "PYTHON_CMD="

REM Verificar ambiente virtual na raiz do projeto
if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
    set "PYTHON_CMD=%SCRIPT_DIR%venv\Scripts\python.exe"
    echo OK - Ambiente virtual encontrado: %SCRIPT_DIR%venv
) else if exist "%SCRIPT_DIR%..\venv\Scripts\python.exe" (
    set "PYTHON_CMD=%SCRIPT_DIR%..\venv\Scripts\python.exe"
    echo OK - Ambiente virtual encontrado no diretorio pai
) else (
    REM Verificar Python do sistema
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERRO: Python nao encontrado!
        echo Por favor, instale o Python ou crie um ambiente virtual.
        echo.
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
    echo OK - Usando Python do sistema
)
echo.

REM Verificar se Django está instalado
echo [5/5] Verificando dependencias...
"%PYTHON_CMD%" -c "import django" >nul 2>&1
if errorlevel 1 (
    echo.
    echo AVISO: Django nao encontrado. Instalando dependencias essenciais...
    echo.
    "%PYTHON_CMD%" -m pip install -q Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 python-dotenv==1.0.0 whitenoise==6.6.0
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao instalar dependencias!
        echo Tentando instalar do requirements.txt...
        "%PYTHON_CMD%" -m pip install -q -r "%SCRIPT_DIR%requirements.txt" 2>nul
        if errorlevel 1 (
            echo.
            echo ERRO: Falha ao instalar dependencias do requirements.txt!
            echo Por favor, instale manualmente: pip install Django djangorestframework django-cors-headers python-dotenv whitenoise
            echo.
            pause
            exit /b 1
        )
    )
    echo OK - Dependencias instaladas
) else (
    REM Verificar outras dependências essenciais
    "%PYTHON_CMD%" -c "import rest_framework" >nul 2>&1
    if errorlevel 1 (
        echo Instalando dependencias adicionais...
        "%PYTHON_CMD%" -m pip install -q djangorestframework==3.14.0 django-cors-headers==4.3.1 python-dotenv==1.0.0 whitenoise==6.6.0
    )
    echo OK - Dependencias encontradas
)
echo.

REM Executar migrações se necessário
echo Verificando banco de dados...
"%PYTHON_CMD%" manage.py migrate --noinput >nul 2>&1
if errorlevel 1 (
    echo AVISO: Algumas migracoes podem ter falhado, mas continuando...
)
echo.

REM Iniciar servidor
echo ================================================================================
echo Servidor iniciando em http://localhost:8000
echo Acesse: http://localhost:8000/admin/
echo.
echo Pressione CTRL+C para parar o servidor
echo ================================================================================
echo.

"%PYTHON_CMD%" manage.py runserver
set "EXIT_CODE=!ERRORLEVEL!"

echo.
echo ================================================================================
if !EXIT_CODE! equ 0 (
    echo Servidor encerrado normalmente.
) else (
    echo Servidor encerrado com codigo de erro: !EXIT_CODE!
    echo.
    echo Possiveis causas:
    echo - Porta 8000 ja esta em uso
    echo - Erro de configuracao do banco de dados
    echo - Dependencias faltando
    echo.
    echo Verifique os erros acima para mais detalhes.
)
echo ================================================================================
echo.
pause
endlocal

