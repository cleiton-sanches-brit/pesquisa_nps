"""
Script para testar conexão com Azure SQL Server
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key

# Carregar variáveis de ambiente
load_dotenv()

def configurar_env():
    """Configura o .env com as credenciais do Azure SQL Server"""
    env_path = Path(".env")
    
    # Credenciais Azure SQL Server
    db_host = "172.190.157.142"
    db_port = "1433"
    db_name = "dbNPS"
    db_user = "user-nps"
    db_password = "0Vda6IxKNQPfn88P"
    
    print("="*60)
    print("Configurando Credenciais Azure SQL Server")
    print("="*60)
    print()
    
    # Atualizar .env
    set_key(str(env_path), "DB_HOST", db_host)
    set_key(str(env_path), "DB_PORT", db_port)
    set_key(str(env_path), "DB_NAME", db_name)
    set_key(str(env_path), "DB_USER", db_user)
    set_key(str(env_path), "DB_PASSWORD", db_password)
    
    print("[OK] Configuracoes atualizadas:")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print()
    
    # Recarregar variáveis
    load_dotenv(override=True)
    
    return db_host, db_port, db_name, db_user, db_password


def testar_conexao_pyodbc():
    """Testa conexão usando pyodbc diretamente"""
    print("="*60)
    print("Teste 1: Conexao Direta com pyodbc")
    print("="*60)
    print()
    
    try:
        import pyodbc
        
        db_host = os.getenv('DB_HOST', '172.190.157.142')
        db_port = os.getenv('DB_PORT', '1433')
        db_name = os.getenv('DB_NAME', 'dbNPS')
        db_user = os.getenv('DB_USER', 'user-nps')
        db_password = os.getenv('DB_PASSWORD', '')
        
        # String de conexão para SQL Server
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_host},{db_port};"
            f"DATABASE={db_name};"
            f"UID={db_user};"
            f"PWD={db_password};"
            f"TrustServerCertificate=yes;"
        )
        
        print(f"Conectando a: {db_host}:{db_port}/{db_name}")
        print()
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Testar query simples
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print("[OK] Conexao estabelecida com sucesso!")
        print()
        print("Informacoes do servidor:")
        print(f"  Versao: {version[:50]}...")
        print()
        
        # Verificar se o banco existe
        cursor.execute("SELECT DB_NAME()")
        current_db = cursor.fetchone()[0]
        print(f"  Banco atual: {current_db}")
        print()
        
        # Listar tabelas existentes
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tabelas = cursor.fetchall()
        
        print(f"Tabelas existentes no banco: {len(tabelas)}")
        if tabelas:
            for tabela in tabelas:
                print(f"  - {tabela[0]}")
        else:
            print("  (Nenhuma tabela encontrada)")
        print()
        
        cursor.close()
        conn.close()
        
        print("[OK] Teste de conexao concluido com sucesso!")
        return True
        
    except ImportError:
        print("[ERRO] pyodbc nao instalado")
        print("  Execute: pip install pyodbc")
        return False
    except Exception as e:
        print(f"[ERRO] Falha na conexao: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_conexao_sqlalchemy():
    """Testa conexão usando SQLAlchemy"""
    print("="*60)
    print("Teste 2: Conexao com SQLAlchemy (FastAPI)")
    print("="*60)
    print()
    
    try:
        from sqlalchemy import create_engine, text
        
        db_host = os.getenv('DB_HOST', '172.190.157.142')
        db_port = os.getenv('DB_PORT', '1433')
        db_name = os.getenv('DB_NAME', 'dbNPS')
        db_user = os.getenv('DB_USER', 'user-nps')
        db_password = os.getenv('DB_PASSWORD', '')
        
        # Connection string para SQL Server
        database_url = (
            f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
        )
        
        print(f"Conectando a: {db_host}:{db_port}/{db_name}")
        print()
        
        engine = create_engine(database_url, echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION"))
            version = result.fetchone()[0]
            
            print("[OK] Conexao estabelecida com sucesso!")
            print()
            print("Informacoes do servidor:")
            print(f"  Versao: {version[:50]}...")
            print()
            
            # Verificar banco atual
            result = conn.execute(text("SELECT DB_NAME()"))
            current_db = result.fetchone()[0]
            print(f"  Banco atual: {current_db}")
            print()
        
        print("[OK] Teste SQLAlchemy concluido com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha na conexao: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_conexao_django():
    """Testa conexão usando Django"""
    print("="*60)
    print("Teste 3: Conexao com Django")
    print("="*60)
    print()
    
    try:
        import django
        from django.conf import settings
        from django.db import connection
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
        
        # Adicionar caminho do Django
        django_path = Path(__file__).resolve().parent / "django_app"
        sys.path.insert(0, str(django_path))
        
        django.setup()
        
        # Testar conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            
            print("[OK] Conexao estabelecida com sucesso!")
            print()
            print("Informacoes do servidor:")
            print(f"  Versao: {version[:50]}...")
            print()
            
            # Verificar banco atual
            cursor.execute("SELECT DB_NAME()")
            current_db = cursor.fetchone()[0]
            print(f"  Banco atual: {current_db}")
            print()
        
        print("[OK] Teste Django concluido com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha na conexao: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    print()
    print("Teste de Conexao Azure SQL Server")
    print()
    
    # Configurar .env
    configurar_env()
    
    print()
    
    # Testar conexões
    resultado1 = testar_conexao_pyodbc()
    print()
    
    if resultado1:
        resultado2 = testar_conexao_sqlalchemy()
        print()
        
        # Teste Django pode falhar se não tiver todas as dependências
        # Mas vamos tentar
        try:
            resultado3 = testar_conexao_django()
        except:
            print("[INFO] Teste Django pulado (pode precisar de configuracao adicional)")
            resultado3 = None
    else:
        resultado2 = False
        resultado3 = None
    
    # Resumo
    print()
    print("="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    print()
    print(f"Teste pyodbc: {'[OK]' if resultado1 else '[ERRO]'}")
    print(f"Teste SQLAlchemy: {'[OK]' if resultado2 else '[ERRO]'}")
    if resultado3 is not None:
        print(f"Teste Django: {'[OK]' if resultado3 else '[ERRO]'}")
    print()
    
    if resultado1 and resultado2:
        print("[OK] Conexao com Azure SQL Server configurada com sucesso!")
        print()
        print("Proximos passos:")
        print("  1. Criar tabelas necessarias")
        print("  2. Executar migracoes do Django")
        print("  3. Testar aplicacoes")
    else:
        print("[ERRO] Alguns testes falharam. Verifique:")
        print("  1. Se pyodbc esta instalado: pip install pyodbc")
        print("  2. Se o ODBC Driver 17 for SQL Server esta instalado")
        print("  3. Se as credenciais estao corretas")
        print("  4. Se o firewall do Azure permite conexoes do seu IP")
    print()


if __name__ == "__main__":
    main()

