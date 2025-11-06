@echo off
echo ============================================================
echo Instalando Dependencias e Iniciando Django
echo ============================================================
echo.

REM Ir para o diretorio do script
cd /d "%~dp0"

echo Verificando ambiente virtual...
if not exist "venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Caminho esperado: venv\Scripts\python.exe
    pause
    exit /b 1
)

echo Python encontrado: venv\Scripts\python.exe
echo.

echo ============================================================
echo Instalando dependencias do requirements.txt...
echo ============================================================
echo.

venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo ============================================================
echo Dependencias instaladas!
echo ============================================================
echo.

echo Entrando na pasta django_app...
cd django_app
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

..\venv\Scripts\python.exe manage.py runserver

pause

