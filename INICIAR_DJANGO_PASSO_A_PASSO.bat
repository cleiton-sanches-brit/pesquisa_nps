@echo off
echo ============================================================
echo Iniciando Servidor Django - Passo a Passo
echo ============================================================
echo.

REM Navegar para o diretorio do projeto
cd /d "%~dp0"

echo Diretorio atual:
cd
echo.

REM Verificar se estamos no lugar certo
if not exist "django_app\manage.py" (
    echo ERRO: Arquivo manage.py nao encontrado!
    echo Certifique-se de que este arquivo esta na raiz do projeto.
    pause
    exit /b 1
)

echo Navegando para django_app...
cd django_app
echo.

REM Verificar se venv existe
if not exist "..\venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Caminho esperado: ..\venv\Scripts\python.exe
    echo.
    echo Verificando caminhos alternativos...
    if exist "..\..\venv\Scripts\python.exe" (
        echo Encontrado em: ..\..\venv\Scripts\python.exe
        set PYTHON_PATH=..\..\venv\Scripts\python.exe
    ) else (
        echo Ambiente virtual nao encontrado em nenhum dos caminhos.
        echo Por favor, verifique se o venv esta instalado.
        pause
        exit /b 1
    )
) else (
    set PYTHON_PATH=..\venv\Scripts\python.exe
)

echo Python encontrado: %PYTHON_PATH%
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

%PYTHON_PATH% manage.py runserver

pause

