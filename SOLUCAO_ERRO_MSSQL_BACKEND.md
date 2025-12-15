# 🔧 Solução: Erro 'mssql' isn't an available database backend

## ❌ Erro

```
django.core.exceptions.ImproperlyConfigured: 'mssql' isn't an available database backend or couldn't be imported.
```

## 🔍 Causa

O Django não consegue encontrar o backend `mssql` do `django-mssql-backend`. Isso pode acontecer porque:

1. O pacote `django-mssql-backend` não está sendo instalado durante o deploy
2. O pacote está instalado mas não está sendo reconhecido pelo Django
3. Há um problema de compatibilidade ou versão

## ✅ Soluções

### Solução 1: Verificar se o pacote está no requirements.txt

Certifique-se de que o `requirements.txt` contém:

```txt
django-mssql-backend==2.8.1
pyodbc==5.0.1
```

### Solução 2: Verificar instalação durante o deploy

No GitHub Actions ou no processo de deploy, verifique se o pacote está sendo instalado:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    # Verificar se foi instalado
    pip list | grep django-mssql-backend
```

### Solução 3: Usar caminho completo do backend

Se o problema persistir, tente usar o caminho completo:

**Arquivo**: `django_app/nps_admin/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',  # ou 'sql_server.pyodbc' se usar django-pyodbc-azure
        # ... resto da configuração
    }
}
```

### Solução 4: Alternativa - Usar django-pyodbc-azure

Se o `django-mssql-backend` continuar dando problemas, você pode usar `django-pyodbc-azure`:

**1. Atualizar requirements.txt:**

```txt
# Remover: django-mssql-backend==2.8.1
# Adicionar:
django-pyodbc-azure==2.1.0.17
```

**2. Atualizar settings.py:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',  # django-pyodbc-azure
        'NAME': os.getenv('DB_NAME', 'dbNPS'),
        'USER': os.getenv('DB_USER', 'user-nps'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '10.1.1.5'),
        'PORT': os.getenv('DB_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
        'CONN_MAX_AGE': 600,
    }
}
```

### Solução 5: Verificar no Azure após deploy

Após o deploy, conecte-se via SSH e verifique:

```bash
cd /home/site/wwwroot/django_app
python -c "import mssql; print('mssql backend OK')"
pip list | grep django-mssql
```

Se não estiver instalado, instale manualmente:

```bash
pip install django-mssql-backend==2.8.1
```

## 🚀 Solução Recomendada (Mais Confiável)

Use `django-pyodbc-azure` que é mais estável e amplamente usado:

### Passo 1: Atualizar requirements.txt

```txt
# SQL Server (Azure SQL)
pyodbc==5.0.1
django-pyodbc-azure==2.1.0.17  # Em vez de django-mssql-backend
```

### Passo 2: Atualizar settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',  # django-pyodbc-azure
        'NAME': os.getenv('DB_NAME', 'dbNPS'),
        'USER': os.getenv('DB_USER', 'user-nps'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '10.1.1.5'),
        'PORT': os.getenv('DB_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
        'CONN_MAX_AGE': 600,
    }
}
```

### Passo 3: Testar localmente

```bash
pip install django-pyodbc-azure==2.1.0.17
python manage.py check
```

### Passo 4: Fazer deploy

```bash
git add requirements.txt django_app/nps_admin/settings.py
git commit -m "Trocar django-mssql-backend por django-pyodbc-azure"
git push origin main
```

## 📋 Checklist

- [ ] `django-mssql-backend` ou `django-pyodbc-azure` está no `requirements.txt`
- [ ] `pyodbc` está no `requirements.txt`
- [ ] O ENGINE está correto no `settings.py`
- [ ] O pacote está sendo instalado durante o deploy
- [ ] ODBC Driver está disponível no Azure (ou será instalado no startup)

## 🔗 Referências

- [django-pyodbc-azure no PyPI](https://pypi.org/project/django-pyodbc-azure/)
- [django-mssql-backend no PyPI](https://pypi.org/project/django-mssql-backend/)
- [Django Database Backends](https://docs.djangoproject.com/en/stable/ref/databases/)

---

**Recomendação**: Use `django-pyodbc-azure` para maior compatibilidade e estabilidade.

