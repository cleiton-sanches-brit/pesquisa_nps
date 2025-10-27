# 🚀 Guia de Instalação - Survey Analytics

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows 10/11** (recomendado)
- **Linux Ubuntu 20.04+** 
- **macOS 10.15+**

### Software Necessário
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **SQL Server 2019+** ([Download](https://www.microsoft.com/en-us/sql-server/sql-server-downloads))
- **Git** ([Download](https://git-scm.com/downloads))
- **Visual Studio Code** ou **Cursor** (recomendado)

### Drivers SQL Server
- **ODBC Driver 17 for SQL Server** ([Download](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))

## 🔧 Instalação Passo a Passo

### 1. Clone do Repositório
```bash
git clone <url-do-repositorio>
cd survey_analytics
```

### 2. Configuração do Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

#### 4.1. Instalar SQL Server
1. Baixe o SQL Server 2019+ do site oficial
2. Execute o instalador
3. Escolha "Basic" para instalação simples
4. Configure uma senha forte para o usuário `sa`
5. Anote as credenciais para uso posterior

#### 4.2. Instalar ODBC Driver
1. Baixe o ODBC Driver 17 for SQL Server
2. Execute o instalador
3. Siga as instruções de instalação

#### 4.3. Configurar Banco de Dados
```bash
# Opção 1: Usar script SQL
sqlcmd -S localhost -i database/init.sql

# Opção 2: Usar SQL Server Management Studio
# 1. Abra o SSMS
# 2. Conecte-se ao servidor local
# 3. Execute o script database/init.sql
```

### 5. Configuração das Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar arquivo .env com suas credenciais
# Windows
notepad .env

# Linux/Mac
nano .env
```

**Conteúdo do arquivo .env:**
```env
# Django Settings
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_HOST=localhost
DB_PORT=1433
DB_NAME=survey_analytics
DB_USER=sa
DB_PASSWORD=sua-senha-do-sql-server

# API Settings
DJANGO_API_URL=http://localhost:8000
FASTAPI_URL=http://localhost:8001
```

### 6. Configuração do Django
```bash
cd dashboard

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 7. Teste de Conexão
```bash
# Voltar para diretório raiz
cd ..

# Testar conexão com banco
python scripts/test_db_connection.py
```

### 8. Executar Aplicações

#### Terminal 1 - Django Dashboard
```bash
cd dashboard
python manage.py runserver
```

#### Terminal 2 - FastAPI Collector
```bash
cd collector
uvicorn main:app --reload --port 8001
```

### 9. Verificar Instalação
- **Django Dashboard**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
- **FastAPI Docs**: http://localhost:8001/docs
- **FastAPI ReDoc**: http://localhost:8001/redoc

## 🐳 Instalação com Docker

### Pré-requisitos Docker
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **Docker Compose** (incluído no Docker Desktop)

### Instalação via Docker
```bash
# Clone do repositório
git clone <url-do-repositorio>
cd survey_analytics

# Configurar variáveis de ambiente
cp env.example .env
# Edite o arquivo .env com suas configurações

# Executar com Docker Compose
docker-compose up -d

# Verificar logs
docker-compose logs -f
```

### Acessar Aplicações Docker
- **Django Dashboard**: http://localhost:8000/
- **FastAPI Collector**: http://localhost:8001/
- **SQL Server**: localhost:1433

## 🔧 Configuração Avançada

### Configuração de Produção

#### 1. Configurações Django
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# Configurações de segurança
SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configurações de banco para produção
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
```

#### 2. Configurações FastAPI
```python
# main.py
app = FastAPI(
    title="Survey Analytics Collector",
    description="API para coleta de respostas de pesquisas",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,  # Desabilitar docs em produção
    redoc_url="/redoc" if DEBUG else None
)
```

#### 3. Configuração de Servidor Web
```nginx
# nginx.conf
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Configuração de Backup

#### 1. Backup do Banco de Dados
```bash
# Backup SQL Server
sqlcmd -S localhost -Q "BACKUP DATABASE survey_analytics TO DISK = 'C:\backup\survey_analytics.bak'"

# Restore
sqlcmd -S localhost -Q "RESTORE DATABASE survey_analytics FROM DISK = 'C:\backup\survey_analytics.bak'"
```

#### 2. Backup de Arquivos
```bash
# Backup dos arquivos do projeto
tar -czf survey_analytics_backup.tar.gz survey_analytics/

# Backup do ambiente virtual
tar -czf venv_backup.tar.gz venv/
```

## 🧪 Testes e Validação

### Testes Automatizados
```bash
# Testes Django
cd dashboard
python manage.py test

# Testes FastAPI
cd collector
pytest

# Testes de integração
python scripts/test_db_connection.py
```

### Validação Manual
1. **Acesse o dashboard**: http://localhost:8000/
2. **Crie uma pesquisa** via admin
3. **Envie uma resposta** via FastAPI
4. **Verifique os dados** no dashboard
5. **Teste a exportação** de dados

### Scripts de Validação
```bash
# Script completo de validação
python scripts/setup_project.py

# Validação de conexão
python scripts/test_db_connection.py

# Iniciar serviços
python scripts/start_services.py
```

## 🚨 Solução de Problemas

### Problemas Comuns

#### 1. Erro de Conexão com Banco
```
Error: [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Login failed
```

**Solução:**
- Verifique as credenciais no arquivo `.env`
- Confirme se o SQL Server está rodando
- Teste a conexão: `python scripts/test_db_connection.py`

#### 2. Erro de Dependências
```
ModuleNotFoundError: No module named 'pyodbc'
```

**Solução:**
```bash
# Reinstalar dependências
pip install -r requirements.txt

# Ou instalar manualmente
pip install pyodbc django-mssql-backend
```

#### 3. Erro de Migrações
```
django.db.utils.OperationalError: (2006, 'MySQL server has gone away')
```

**Solução:**
```bash
# Recriar migrações
cd dashboard
rm -rf migrations/
python manage.py makemigrations
python manage.py migrate
```

#### 4. Erro de Porta em Uso
```
OSError: [Errno 98] Address already in use
```

**Solução:**
```bash
# Encontrar processo usando a porta
netstat -tulpn | grep :8000
netstat -tulpn | grep :8001

# Matar processo
kill -9 <PID>

# Ou usar portas diferentes
python manage.py runserver 8002
uvicorn main:app --port 8003
```

### Logs e Debug

#### 1. Habilitar Logs Detalhados
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

#### 2. Debug de Conexão
```python
# Teste de conexão manual
import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost,1433;'
        'DATABASE=survey_analytics;'
        'UID=sa;'
        'PWD=sua-senha;'
        'TrustServerCertificate=yes;'
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro de conexão: {e}")
```

## 📞 Suporte

### Recursos de Ajuda
- **Documentação**: Consulte os arquivos em `docs/`
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/survey_analytics/issues)
- **Logs**: Verifique os logs de erro para diagnóstico

### Informações para Suporte
Ao solicitar suporte, inclua:
1. **Sistema operacional** e versão
2. **Versão do Python** (`python --version`)
3. **Versão do SQL Server** (`sqlcmd -S localhost -Q "SELECT @@VERSION"`)
4. **Logs de erro** completos
5. **Passos para reproduzir** o problema

---

*Este guia cobre a instalação completa do Survey Analytics em diferentes ambientes.*
