# Configuração para Azure SQL Server
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do Azure SQL Server
AZURE_SQL_CONFIG = {
    'ENGINE': 'mssql',
    'NAME': os.getenv('AZURE_DB_NAME', 'seu_banco_azure'),
    'USER': os.getenv('AZURE_DB_USER', 'seu_usuario_azure'),
    'PASSWORD': os.getenv('AZURE_DB_PASSWORD', 'sua_senha_azure'),
    'HOST': os.getenv('AZURE_DB_HOST', 'seu_servidor_azure.database.windows.net'),
    'PORT': os.getenv('AZURE_DB_PORT', '1433'),
    'OPTIONS': {
        'driver': 'ODBC Driver 17 for SQL Server',
        'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    }
}

# String de conexão para Azure
AZURE_CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={AZURE_SQL_CONFIG['HOST']},{AZURE_SQL_CONFIG['PORT']};"
    f"DATABASE={AZURE_SQL_CONFIG['NAME']};"
    f"UID={AZURE_SQL_CONFIG['USER']};"
    f"PWD={AZURE_SQL_CONFIG['PASSWORD']};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

