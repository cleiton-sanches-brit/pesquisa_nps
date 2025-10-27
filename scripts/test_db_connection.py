#!/usr/bin/env python3
"""
Script para testar a conexão com o SQL Server
"""
import os
import sys
import pyodbc
from dotenv import load_dotenv

def test_connection():
    """Testa a conexão com o SQL Server"""
    print("🔍 Testando conexão com SQL Server...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Obter configurações do banco
    server = os.getenv('DB_HOST', 'localhost')
    database = os.getenv('DB_NAME', 'nps_surveys')
    username = os.getenv('DB_USER', '')
    password = os.getenv('DB_PASSWORD', '')
    port = os.getenv('DB_PORT', '1433')
    
    if not username or not password:
        print("❌ Usuário ou senha do banco não configurados no arquivo .env")
        return False
    
    try:
        # String de conexão
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server},{port};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        
        print(f"📡 Conectando em: {server}:{port}")
        print(f"🗄️  Banco: {database}")
        print(f"👤 Usuário: {username}")
        
        # Tentar conectar
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Testar consulta simples
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print("✅ Conexão estabelecida com sucesso!")
        print(f"📊 Versão do SQL Server: {version[:50]}...")
        
        # Fechar conexão
        cursor.close()
        connection.close()
        
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    print("🧪 Teste de Conexão SQL Server")
    print("=" * 40)
    
    # Verificar se o arquivo .env existe
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado.")
        print("📝 Copie o arquivo env.example para .env e configure suas credenciais.")
        return
    
    success = test_connection()
    
    if success:
        print("\n🎉 Teste concluído com sucesso!")
        print("✅ O banco está pronto para uso.")
    else:
        print("\n💡 Dicas para resolver problemas:")
        print("1. Verifique se o SQL Server está rodando")
        print("2. Confirme as credenciais no arquivo .env")
        print("3. Verifique se o ODBC Driver 17 está instalado")
        print("4. Teste a conectividade de rede")

if __name__ == "__main__":
    main()
