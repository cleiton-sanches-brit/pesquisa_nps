#!/bin/bash

# Script de inicialização para Azure App Service
# Este script é executado automaticamente pelo Azure ao iniciar o container

echo "=== Iniciando aplicação Django no Azure App Service ==="

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



