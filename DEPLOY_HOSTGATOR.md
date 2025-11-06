# 🚀 Guia de Deploy no Hostgator

## ⚠️ Importante: Limitações do Hostgator

O Hostgator é uma hospedagem compartilhada tradicional que:
- ✅ Suporta Python/Django (dependendo do plano)
- ⚠️ Pode ter limitações de recursos
- ⚠️ Geralmente não suporta PostgreSQL (apenas MySQL)
- ⚠️ Pode precisar de configuração manual via cPanel

## 📋 Pré-requisitos

1. **Plano Hostgator com suporte a Python**
   - Verifique se seu plano inclui Python
   - Alguns planos só têm PHP/MySQL

2. **Acesso ao cPanel**
   - Login no cPanel do Hostgator

3. **Acesso via FTP/SFTP**
   - Para enviar arquivos

---

## 🔍 Passo 1: Verificar Suporte a Python/Django

### 1.1 Verificar no cPanel

1. Acesse o cPanel do Hostgator
2. Procure por:
   - **"Python App"** ou **"Python Selector"**
   - **"Setup Python App"**
   - Se não encontrar, seu plano pode não suportar Python

### 1.2 Verificar Versão do Python

No cPanel, verifique qual versão do Python está disponível:
- Python 3.8+ é recomendado
- Django 4.2 requer Python 3.8+

---

## 📦 Passo 2: Preparar Arquivos para Upload

### 2.1 Estrutura de Arquivos

Você precisará enviar:
- Todo o diretório `django_app/`
- `requirements.txt`
- `Procfile` (pode precisar ajustar)
- `.env` (com variáveis de ambiente) - **NÃO ENVIE COM SENHAS REAIS**

### 2.2 Arquivos a NÃO Enviar

- `venv/` (ambiente virtual)
- `__pycache__/`
- `*.pyc`
- `.git/`
- `db.sqlite3` (se houver)

---

## 🔧 Passo 3: Configurar Aplicação Python no cPanel

### 3.1 Criar Aplicação Python

1. No cPanel, vá em **"Python App"** ou **"Setup Python App"**
2. Clique em **"Create Application"**
3. Configure:
   - **Python Version:** 3.8 ou superior
   - **Application Root:** `/home/usuario/public_html/pesquisa_nps` (ou onde você quer)
   - **Application URL:** `/` ou `/pesquisa_nps`
   - **Application Startup File:** `django_app/nps_admin/wsgi.py`

### 3.2 Instalar Dependências

Após criar a aplicação:
1. O cPanel criará um ambiente virtual
2. Ative o ambiente virtual
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Passo 4: Configurar Banco de Dados

### 4.1 Opção A: Usar MySQL do Hostgator (Recomendado)

O Hostgator geralmente oferece MySQL, não PostgreSQL. Você precisará:

1. **Criar banco MySQL no cPanel:**
   - Vá em **"MySQL Databases"**
   - Crie um novo banco
   - Crie um usuário
   - Associe usuário ao banco

2. **Ajustar settings.py para MySQL:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'nome_do_banco',
           'USER': 'usuario_mysql',
           'PASSWORD': 'senha_mysql',
           'HOST': 'localhost',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           },
       }
   }
   ```

3. **Instalar mysqlclient:**
   ```bash
   pip install mysqlclient
   ```

### 4.2 Opção B: Continuar com Supabase (PostgreSQL)

Se o Hostgator permitir conexões externas:
- Use as mesmas configurações do Supabase
- Verifique se o IP do Hostgator está na whitelist do Supabase

---

## 📝 Passo 5: Configurar Variáveis de Ambiente

### 5.1 Via cPanel

1. Na aplicação Python criada, procure por **"Environment Variables"**
2. Adicione as variáveis necessárias:
   ```
   SECRET_KEY=sua-chave-secreta
   DEBUG=False
   ALLOWED_HOSTS=seudominio.com,www.seudominio.com
   DB_HOST=localhost
   DB_NAME=nome_do_banco
   DB_USER=usuario_mysql
   DB_PASSWORD=senha_mysql
   ```

### 5.2 Via Arquivo .env

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione as variáveis (sem aspas):
   ```
   SECRET_KEY=sua-chave-secreta
   DEBUG=False
   ALLOWED_HOSTS=seudominio.com,www.seudominio.com
   ```

---

## 🚀 Passo 6: Configurar WSGI

### 6.1 Arquivo passenger_wsgi.py (se necessário)

Alguns planos Hostgator usam Passenger. Crie `passenger_wsgi.py` na raiz:

```python
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')

# Importar aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6.2 Ajustar settings.py

Certifique-se de que `ALLOWED_HOSTS` inclui seu domínio:
```python
ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']
```

---

## 📤 Passo 7: Fazer Upload dos Arquivos

### 7.1 Via FTP/SFTP

1. Use FileZilla ou similar
2. Conecte ao servidor Hostgator
3. Navegue até o diretório da aplicação Python
4. Faça upload de todos os arquivos

### 7.2 Via cPanel File Manager

1. Acesse **"File Manager"** no cPanel
2. Navegue até o diretório da aplicação
3. Faça upload dos arquivos

---

## 🔄 Passo 8: Executar Migrações

1. No cPanel, vá em **"Terminal"** ou use SSH
2. Ative o ambiente virtual da aplicação Python
3. Execute:
   ```bash
   cd django_app
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

---

## ⚠️ Problemas Comuns no Hostgator

### "Python não encontrado"
- Verifique se seu plano suporta Python
- Entre em contato com suporte Hostgator

### "Erro ao instalar dependências"
- Alguns pacotes podem não estar disponíveis
- Tente instalar manualmente via pip

### "Banco de dados não conecta"
- Verifique se MySQL está rodando
- Confirme credenciais no cPanel

### "Arquivos estáticos não carregam"
- Execute `collectstatic`
- Configure STATIC_ROOT no settings.py

---

## 💡 Alternativas Gratuitas ao Railway

Se o Hostgator não funcionar, considere:

### 1. **Render.com** (Gratuito)
- ✅ Deploy automático do GitHub
- ✅ Suporta PostgreSQL
- ✅ HTTPS automático
- ⚠️ Pode hibernar após 15min sem uso

### 2. **Fly.io** (Gratuito)
- ✅ Muito rápido
- ✅ Suporta PostgreSQL
- ⚠️ Requer CLI

### 3. **PythonAnywhere** (Gratuito)
- ✅ Especializado em Python
- ✅ Fácil de usar
- ⚠️ Limitações no plano gratuito

### 4. **Heroku** (Pago)
- ✅ Muito popular
- ❌ Não tem mais plano gratuito

---

## 📚 Próximos Passos

1. Verifique se seu plano Hostgator suporta Python
2. Se sim, siga os passos acima
3. Se não, considere alternativas gratuitas (Render, Fly.io)

---

**Recomendação:** Se o Hostgator não suportar Python bem, considere usar **Render.com** que é gratuito e muito mais fácil para Django!

