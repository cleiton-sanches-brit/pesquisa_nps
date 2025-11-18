"""
Diagnóstico detalhado de conexão com Azure SQL Server
"""
import os
import socket
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def verificar_porta_aberta():
    """Verifica se a porta está acessível"""
    print("="*60)
    print("Diagnostico de Conexao")
    print("="*60)
    print()
    
    db_host = os.getenv('DB_HOST', '172.190.157.142')
    db_port = int(os.getenv('DB_PORT', '1433'))
    
    print(f"1. Verificando conectividade de rede...")
    print(f"   Host: {db_host}")
    print(f"   Porta: {db_port}")
    print()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((db_host, db_port))
        sock.close()
        
        if result == 0:
            print(f"   [OK] Porta {db_port} esta acessivel")
        else:
            print(f"   [ERRO] Porta {db_port} nao esta acessivel")
            print(f"   Possiveis causas:")
            print(f"   - Firewall do Azure bloqueando seu IP")
            print(f"   - Servidor nao esta rodando")
            print(f"   - Porta incorreta")
        print()
        return result == 0
    except Exception as e:
        print(f"   [ERRO] Erro ao verificar porta: {e}")
        print()
        return False


def verificar_credenciais():
    """Mostra as credenciais (sem senha completa)"""
    print("2. Verificando credenciais configuradas...")
    print()
    
    db_host = os.getenv('DB_HOST', '172.190.157.142')
    db_port = os.getenv('DB_PORT', '1433')
    db_name = os.getenv('DB_NAME', 'dbNPS')
    db_user = os.getenv('DB_USER', 'user-nps')
    db_password = os.getenv('DB_PASSWORD', '')
    
    print(f"   Host: {db_host}")
    print(f"   Porta: {db_port}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Password: {'*' * len(db_password) if db_password else 'NAO CONFIGURADA'}")
    print()
    
    if not db_password:
        print("   [ERRO] Senha nao configurada!")
        return False
    
    return True


def tentar_conexao_com_timeout_maior():
    """Tenta conexão com timeout maior"""
    print("3. Tentando conexao com timeout maior (30 segundos)...")
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
        
        print(f"   Conectando...")
        conn = pyodbc.connect(connection_string, timeout=30)
        cursor = conn.cursor()
        
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print(f"   [OK] Conexao estabelecida!")
        print(f"   Versao: {version[:50]}...")
        print()
        
        cursor.close()
        conn.close()
        return True
        
    except pyodbc.OperationalError as e:
        print(f"   [ERRO] Erro de conexao: {e}")
        print()
        print("   POSSIVEIS SOLUCOES:")
        print("   1. Verificar se o firewall do Azure permite seu IP")
        print("   2. No Azure Portal, adicionar seu IP nas regras de firewall")
        print("   3. Verificar se o servidor SQL esta rodando")
        print("   4. Verificar se a porta 1433 esta aberta")
        return False
    except Exception as e:
        print(f"   [ERRO] Erro: {e}")
        return False


def instrucoes_azure_firewall():
    """Instruções para configurar firewall do Azure"""
    print("="*60)
    print("CONFIGURAR FIREWALL DO AZURE")
    print("="*60)
    print()
    print("O erro de timeout geralmente indica que o firewall")
    print("do Azure esta bloqueando conexoes do seu IP.")
    print()
    print("SOLUCAO:")
    print("1. Acesse o Azure Portal:")
    print("   https://portal.azure.com/")
    print()
    print("2. Vá em SQL Servers > Seu servidor SQL")
    print()
    print("3. No menu lateral, clique em 'Networking' ou 'Firewall'")
    print()
    print("4. Adicione uma regra de firewall:")
    print("   - Clique em 'Add client IP' OU")
    print("   - Adicione manualmente seu IP publico")
    print()
    print("5. Salve as alteracoes")
    print()
    print("6. Aguarde alguns minutos para propagacao")
    print()
    print("7. Tente conectar novamente")
    print()
    print("NOTA: Seu IP publico atual pode ser obtido em:")
    print("   https://www.whatismyip.com/")
    print()


def main():
    print()
    print("Diagnostico de Conexao Azure SQL Server")
    print()
    
    # Verificar porta
    porta_ok = verificar_porta_aberta()
    
    # Verificar credenciais
    credenciais_ok = verificar_credenciais()
    
    if porta_ok and credenciais_ok:
        # Tentar conexão
        conexao_ok = tentar_conexao_com_timeout_maior()
        
        if not conexao_ok:
            instrucoes_azure_firewall()
    else:
        if not porta_ok:
            print()
            print("="*60)
            print("PROBLEMA IDENTIFICADO")
            print("="*60)
            print()
            print("A porta nao esta acessivel. Isso geralmente significa:")
            print("1. Firewall do Azure bloqueando seu IP")
            print("2. Servidor nao esta rodando")
            print("3. Porta incorreta")
            print()
            instrucoes_azure_firewall()
        
        if not credenciais_ok:
            print()
            print("Verifique as credenciais no arquivo .env")
    
    print()


if __name__ == "__main__":
    main()

