"""
Script para executar os scripts SQL no Supabase
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def execute_sql_file(conn, file_path):
    """Executa um arquivo SQL no banco de dados"""
    try:
        print(f"\nExecutando: {file_path.name}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por ponto e vírgula (comentários podem ter ; dentro)
        # Mas vamos executar tudo de uma vez
        cursor = conn.cursor()
        cursor.execute(sql_content)
        conn.commit()
        cursor.close()
        
        print(f"OK: {file_path.name} executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"ERRO ao executar {file_path.name}: {str(e)}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("EXECUTANDO SCRIPTS SQL NO SUPABASE")
    print("=" * 60)
    
    # Verificar se psycopg2 está instalado
    try:
        import psycopg2
    except ImportError:
        print("\nERRO: psycopg2 nao instalado!")
        print("Instale com: pip install psycopg2-binary")
        return False
    
    # Obter credenciais
    db_host = os.getenv('DB_HOST', '')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    db_port = os.getenv('DB_PORT', '5432')
    
    if not db_host or not db_password:
        print("\nERRO: Credenciais nao configuradas no .env!")
        return False
    
    print(f"\nConectando ao Supabase...")
    print(f"Host: {db_host}:{db_port}")
    print(f"Database: {db_name}")
    
    # Conectar ao banco
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
            sslmode='require'
        )
        print("OK: Conectado ao Supabase!")
    except Exception as e:
        print(f"ERRO ao conectar: {str(e)}")
        return False
    
    # Executar scripts SQL
    project_root = Path(__file__).resolve().parent.parent
    scripts = [
        project_root / 'database' / 'tabela_respondents.sql',
        project_root / 'database' / 'powerbi_views.sql',
    ]
    
    success_count = 0
    for script_path in scripts:
        if script_path.exists():
            if execute_sql_file(conn, script_path):
                success_count += 1
        else:
            print(f"AVISO: Arquivo nao encontrado: {script_path}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"RESUMO: {success_count}/{len(scripts)} scripts executados com sucesso")
    print("=" * 60)
    
    if success_count == len(scripts):
        print("\nTodas as tabelas e views foram criadas com sucesso!")
        return True
    else:
        print("\nAlguns scripts falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
