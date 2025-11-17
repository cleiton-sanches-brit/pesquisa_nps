@echo off
echo ============================================
echo Iniciando FastAPI - NPS Surveys API
echo ============================================
echo.

cd pesquisas_nps\fastapi_app
..\..\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

pause

