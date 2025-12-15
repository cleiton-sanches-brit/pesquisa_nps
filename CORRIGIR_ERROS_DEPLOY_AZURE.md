# 🔧 Correção de Erros de Deploy no Azure

Este documento descreve os erros encontrados durante o deploy e como corrigi-los.

---

## ❌ Erro Encontrado

```
RuntimeError: Model class django.contrib.sites.models.Site doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
```

E também:

```
ImproperlyConfigured: 'mssql' isn't an available database backend or couldn't be imported.
```

---

## ✅ Correções Aplicadas

### 1. Adicionado `django.contrib.sites` ao INSTALLED_APPS

**Arquivo**: `django_app/nps_admin/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # ✅ ADICIONADO
    'rest_framework',
    'corsheaders',
    'surveys',
]
```

### 2. Adicionado `SITE_ID` nas configurações

**Arquivo**: `django_app/nps_admin/settings.py`

```python
# Django Sites Framework
SITE_ID = 1  # ✅ ADICIONADO
```

### 3. Corrigido o ENGINE do banco de dados

**Arquivo**: `django_app/nps_admin/settings.py`

**Antes:**
```python
'ENGINE': 'sql_server.pyodbc',  # ❌ ERRADO
```

**Depois:**
```python
'ENGINE': 'mssql',  # ✅ CORRETO (usa django-mssql-backend)
```

---

## 🔍 Problemas Adicionais que Podem Ocorrer no Deploy

### Problema 1: ODBC Driver não instalado no Azure

O Azure App Service Linux **não tem o ODBC Driver instalado por padrão**. Você precisa instalá-lo.

#### Solução: Adicionar ao startup.sh

**Arquivo**: `startup.sh`

Adicione antes de executar as migrations:

```bash
#!/bin/bash

echo "=== Instalando ODBC Driver para SQL Server ==="

# Instalar ODBC Driver 17 for SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

echo "=== ODBC Driver instalado ==="

# Resto do script...
cd /home/site/wwwroot/django_app || exit 1
# ...
```

**⚠️ IMPORTANTE**: Isso pode tornar o startup mais lento. Considere usar uma imagem Docker customizada.

### Problema 2: Caminho do requirements.txt no GitHub Actions

**Arquivo**: `.github/workflows/azure-deploy.yml`

Verifique se o caminho está correto:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt  # ✅ Verifique se está no caminho correto
```

### Problema 3: Variáveis de ambiente não configuradas

Certifique-se de que todas as variáveis estão configuradas no Azure Portal:

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

---

## 🚀 Passos para Corrigir o Deploy

### Passo 1: Fazer commit das alterações

```bash
git add django_app/nps_admin/settings.py
git commit -m "Corrigir configuração de banco de dados e adicionar django.contrib.sites"
git push origin main
```

### Passo 2: Verificar se o ODBC Driver está disponível no Azure

No Azure Portal:
1. Vá em **App Service** → **SSH** ou **Console**
2. Execute: `odbcinst -j`
3. Se não estiver instalado, adicione ao `startup.sh` (veja Problema 1)

### Passo 3: Configurar variáveis de ambiente

No Azure Portal:
1. Vá em **App Service** → **Configuration** → **Application settings**
2. Adicione todas as variáveis necessárias
3. Clique em **Save**

### Passo 4: Executar migrações manualmente (se necessário)

Via SSH do Azure:

```bash
cd /home/site/wwwroot/django_app
python manage.py migrate
python manage.py createsuperuser
```

### Passo 5: Verificar logs

No Azure Portal:
1. Vá em **App Service** → **Log stream**
2. Verifique se há erros durante o startup
3. Vá em **Logs** → **Application Logs** para ver erros da aplicação

---

## 🔄 Alternativa: Usar Dockerfile

Se o ODBC Driver continuar dando problemas, considere usar um Dockerfile:

**Arquivo**: `Dockerfile`

```dockerfile
FROM python:3.12-slim

# Instalar ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY django_app /app/django_app
WORKDIR /app/django_app

# Expor porta
EXPOSE 8000

# Comando de startup
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "600", "nps_admin.wsgi:application"]
```

---

## 📋 Checklist de Verificação

Antes de fazer deploy, verifique:

- [ ] `django.contrib.sites` está em `INSTALLED_APPS`
- [ ] `SITE_ID = 1` está configurado
- [ ] `ENGINE` está como `'mssql'` (não `'sql_server.pyodbc'`)
- [ ] `django-mssql-backend==2.8.1` está no `requirements.txt`
- [ ] `pyodbc==5.0.1` está no `requirements.txt`
- [ ] Variáveis de ambiente estão configuradas no Azure
- [ ] ODBC Driver está instalado (ou será instalado no startup)
- [ ] Migrações foram executadas
- [ ] Site padrão foi criado (se necessário)

---

## 🆘 Troubleshooting

### Erro: "ODBC Driver 17 for SQL Server not found"

**Solução**: Instale o driver no startup.sh ou use Dockerfile.

### Erro: "Connection timeout"

**Solução**: 
1. Verifique o firewall do SQL Server
2. Adicione o IP do App Service às regras de firewall
3. Ative "Permitir serviços do Azure"

### Erro: "Authentication failed"

**Solução**:
1. Verifique `DB_USER` e `DB_PASSWORD`
2. Certifique-se de que o usuário tem permissões no banco
3. Verifique se o banco existe

---

## 📚 Referências

- [django-mssql-backend Documentation](https://github.com/ESSolutions/django-mssql-backend)
- [Azure App Service - Python](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

**Última atualização**: 2024

