"""
Script para testar conexão com Supabase PostgreSQL
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente
load_dotenv()

def test_connection():
    """Testa a conexão com o banco de dados Supabase"""
    print("=" * 60)
    print("TESTE DE CONEXÃO COM SUPABASE POSTGRESQL")
    print("=" * 60)
    
    # Verificar se as variáveis estão configuradas
    db_host = os.getenv('DB_HOST', '')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    db_port = os.getenv('DB_PORT', '5432')
    
    if not db_host or not db_password:
        print("\nERRO: Variaveis de ambiente nao configuradas!")
        print("\nConfigure no arquivo .env:")
        print("DB_HOST=db.xxxxxxxxxxxxx.supabase.co")
        print("DB_PORT=5432")
        print("DB_NAME=postgres")
        print("DB_USER=postgres")
        print("DB_PASSWORD=sua_senha_aqui")
        return False
    
    print(f"\nConfiguracoes:")
    print(f"   Host: {db_host}")
    print(f"   Porta: {db_port}")
    print(f"   Banco: {db_name}")
    print(f"   Usuario: {db_user}")
    
    # Tentar importar psycopg2
    try:
        import psycopg2
        from psycopg2 import sql
        print("\nOK: Modulo psycopg2 encontrado")
    except ImportError:
        print("\nERRO: psycopg2 nao instalado!")
        print("\nInstale com:")
        print("   pip install psycopg2-binary")
        return False
    
    # Tentar conectar
    print("\nTentando conectar...")
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
            sslmode='require'
        )
        print("OK: Conexao estabelecida com sucesso!")
        
        # Verificar versão do PostgreSQL
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\nVersao do PostgreSQL: {version[:50]}...")
        
        # Verificar tabelas do surveys
        print("\nVerificando tabelas do sistema surveys:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'surveys_%'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        expected_tables = [
            'surveys_answer',
            'surveys_choice',
            'surveys_npsresult',
            'surveys_question',
            'surveys_survey',
            'surveys_surveyinvitation',
            'surveys_surveyresponse'
        ]
        
        existing_tables = [table[0] for table in tables]
        missing_tables = [t for t in expected_tables if t not in existing_tables]
        
        if existing_tables:
            print(f"\nOK: Tabelas encontradas ({len(existing_tables)}/7):")
            for table in existing_tables:
                print(f"   - {table}")
        else:
            print("\nAVISO: Nenhuma tabela surveys encontrada!")
            print("   Execute o script supabase_schema.sql no Supabase SQL Editor")
        
        if missing_tables:
            print(f"\nERRO: Tabelas faltando ({len(missing_tables)}):")
            for table in missing_tables:
                print(f"   X {table}")
            return False
        
        # Verificar foreign keys
        print("\nVerificando foreign keys...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY'
            AND table_name LIKE 'surveys_%';
        """)
        fk_count = cursor.fetchone()[0]
        print(f"   OK: {fk_count} foreign keys encontradas")
        
        # Verificar índices
        print("\nVerificando indices...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM pg_indexes 
            WHERE schemaname = 'public'
            AND tablename LIKE 'surveys_%';
        """)
        index_count = cursor.fetchone()[0]
        print(f"   OK: {index_count} indices encontrados")
        
        # Verificar extensão UUID
        print("\nVerificando extensao UUID...")
        cursor.execute("""
            SELECT EXISTS(
                SELECT 1 FROM pg_extension WHERE extname = 'uuid-ossp'
            );
        """)
        uuid_ext = cursor.fetchone()[0]
        if uuid_ext:
            print("   OK: Extensao uuid-ossp habilitada")
        else:
            print("   AVISO: Extensao uuid-ossp nao encontrada (pode ser necessario)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("TESTE CONCLUIDO COM SUCESSO!")
        print("=" * 60)
        print("\nO banco de dados está configurado corretamente.")
        print("Você pode prosseguir com a configuração do Django.")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\nERRO DE CONEXAO: {str(e)}")
        print("\nVerifique:")
        print("   1. Se as credenciais estao corretas no .env")
        print("   2. Se o Supabase esta acessivel")
        print("   3. Se o firewall permite conexoes")
        return False
    except Exception as e:
        print(f"\nERRO INESPERADO: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
