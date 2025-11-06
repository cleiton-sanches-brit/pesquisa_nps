@echo off
echo ============================================
echo Exportando Preview de Email para PDF/PNG
echo ============================================
echo.

cd pesquisas_nps
..\venv\Scripts\python.exe exportar_preview_email.py

echo.
echo Exportacao concluida!
echo Verifique a pasta 'exports' para os arquivos gerados.
echo.
pause

