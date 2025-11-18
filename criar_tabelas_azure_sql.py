"""
Script para criar tabelas no Azure SQL Server após conexão estar disponível
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def testar_conexao():
    """Testa se a conexão está disponível"""
    print("="*60)
    print("Testando Conexao com Azure SQL Server")
    print("="*60)
    print()
    
    try:
        import pyodbc
        
        db_host = os.getenv('DB_HOST', '172.190.157.142')
        db_port = os.getenv('DB_PORT', '1433')
        db_name = os.getenv('DB_NAME', 'dbNPS')
        db_user = os.getenv('DB_USER', 'user-nps')
        db_password = os.getenv('DB_PASSWORD', '')
        
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_host},{db_port};"
            f"DATABASE={db_name};"
            f"UID={db_user};"
            f"PWD={db_password};"
            f"TrustServerCertificate=yes;"
            f"Connection Timeout=30;"
        )
        
        print(f"Conectando a: {db_host}:{db_port}/{db_name}...")
        conn = pyodbc.connect(connection_string, timeout=30)
        cursor = conn.cursor()
        
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print("[OK] Conexao estabelecida!")
        print(f"Versao: {version[:50]}...")
        print()
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha na conexao: {e}")
        print()
        print("SOLUCAO:")
        print("1. Configure o firewall do Azure para permitir seu IP")
        print("2. Acesse: https://portal.azure.com/")
        print("3. Vá em SQL Servers > Networking > Adicione seu IP")
        print("4. Execute este script novamente")
        print()
        return False


def criar_tabelas_django():
    """Cria tabelas usando migrações do Django"""
    print("="*60)
    print("Criando Tabelas do Django")
    print("="*60)
    print()
    
    try:
        # Adicionar caminho do Django
        django_path = Path(__file__).resolve().parent / "django_app"
        sys.path.insert(0, str(django_path))
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
        
        import django
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.db import connection
        
        print("[INFO] Executando migracoes do Django...")
        print()
        
        # Executar makemigrations
        print("1. Criando arquivos de migracao...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        print()
        
        # Executar migrate
        print("2. Aplicando migracoes...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print()
        
        # Verificar tabelas criadas
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME LIKE 'surveys_%'
                ORDER BY TABLE_NAME
            """)
            tabelas = cursor.fetchall()
            
            print(f"[OK] Tabelas Django criadas: {len(tabelas)}")
            for tabela in tabelas:
                print(f"  - {tabela[0]}")
            print()
        
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar tabelas Django: {e}")
        import traceback
        traceback.print_exc()
        return False


def verificar_tabelas_existentes():
    """Lista todas as tabelas existentes no banco"""
    print("="*60)
    print("Tabelas Existentes no Banco")
    print("="*60)
    print()
    
    try:
        import pyodbc
        
        db_host = os.getenv('DB_HOST', '172.190.157.142')
        db_port = os.getenv('DB_PORT', '1433')
        db_name = os.getenv('DB_NAME', 'dbNPS')
        db_user = os.getenv('DB_USER', 'user-nps')
        db_password = os.getenv('DB_PASSWORD', '')
        
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_host},{db_port};"
            f"DATABASE={db_name};"
            f"UID={db_user};"
            f"PWD={db_password};"
            f"TrustServerCertificate=yes;"
        )
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        tabelas = cursor.fetchall()
        
        print(f"Total de tabelas: {len(tabelas)}")
        print()
        
        if tabelas:
            for tabela in tabelas:
                print(f"  - {tabela[0]}")
        else:
            print("  (Nenhuma tabela encontrada)")
        print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[ERRO] Erro ao listar tabelas: {e}")


def main():
    """Função principal"""
    print()
    print("Criacao de Tabelas no Azure SQL Server")
    print()
    
    # Testar conexão
    if not testar_conexao():
        return
    
    print()
    
    # Verificar tabelas existentes
    verificar_tabelas_existentes()
    
    print()
    
    # Criar tabelas Django
    if criar_tabelas_django():
        print()
        print("="*60)
        print("RESUMO")
        print("="*60)
        print()
        print("[OK] Tabelas criadas com sucesso!")
        print()
        print("Proximos passos:")
        print("  1. Verificar tabelas no banco de dados")
        print("  2. Testar aplicacoes Django e FastAPI")
        print("  3. Criar superusuario: python manage.py createsuperuser")
        print()
    else:
        print()
        print("[ERRO] Falha ao criar tabelas")
        print()
    
    # Verificar tabelas finais
    print()
    verificar_tabelas_existentes()


if __name__ == "__main__":
    main()

