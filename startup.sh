#!/bin/bash

# Script de inicialização para Azure App Service
# Este script é executado automaticamente pelo Azure ao iniciar o container

echo "=== Iniciando aplicação Django no Azure App Service ==="

# Verificar e instalar ODBC Driver se necessário
if ! command -v odbcinst &> /dev/null; then
    echo "=== Instalando ODBC Driver para SQL Server ==="
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - 2>/dev/null || true
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list 2>/dev/null || true
    apt-get update -qq
    ACCEPT_EULA=Y apt-get install -y -qq msodbcsql17 unixodbc-dev 2>/dev/null || echo "Aviso: Não foi possível instalar ODBC Driver automaticamente"
    echo "=== ODBC Driver verificado ==="
fi

# Navegar para o diretório da aplicação Django
cd /home/site/wwwroot/django_app || exit 1

echo "Diretório atual: $(pwd)"

# Executar migrations
echo "Executando migrations do banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Verificar se há erros nas migrations ou collectstatic
if [ $? -ne 0 ]; then
    echo "ERRO: Falha ao executar migrations ou collectstatic"
    exit 1
fi

echo "=== Iniciando servidor Gunicorn ==="

# Iniciar Gunicorn
# O Azure App Service expõe a porta através da variável PORT
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 600 --access-logfile - --error-logfile - nps_admin.wsgi:application



