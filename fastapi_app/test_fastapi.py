#!/usr/bin/env python3
"""
Script para testar se o FastAPI pode ser importado e iniciado
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("Testando imports do FastAPI...")
    from fastapi_app.database import engine, get_db
    print("OK - Database importado com sucesso")
    
    from fastapi_app.models import Survey, Question, SurveyResponse
    print("OK - Models importados com sucesso")
    
    from fastapi_app.main import app
    print("OK - FastAPI app criado com sucesso")
    
    print("\nOK - Todos os imports funcionaram!")
    print("\nPara iniciar o FastAPI, execute:")
    print("cd fastapi_app")
    print("python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload")
    
except Exception as e:
    print(f"\nERRO ao importar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

