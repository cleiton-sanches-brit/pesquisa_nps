# 🚀 Guia de Deploy no Railway.app

## ✅ Checklist Pré-Deploy

- [x] Repositório no GitHub conectado
- [x] Procfile configurado
- [x] requirements.txt atualizado
- [x] runtime.txt configurado
- [x] WhiteNoise configurado para arquivos estáticos
- [x] Settings.py configurado para produção

---

## 📋 Passo 1: Configurar Variáveis de Ambiente no Railway

No dashboard do Railway, vá em **"Variables"** e adicione todas as variáveis abaixo:

### 🔐 Configurações Django

```
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DEBUG=False
ALLOWED_HOSTS=*.railway.app,seu-app.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://seu-app.railway.app
```

**⚠️ IMPORTANTE:**
- Gere uma SECRET_KEY segura: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- Substitua `seu-app.railway.app` pelo domínio real do seu app no Railway

### 🗄️ Configurações do Banco de Dados (Supabase)

```
DB_HOST=aws-1-us-east-2.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.pzumhkxjasqntwujdztg
DB_PASSWORD=Pds2025@@
```

**⚠️ IMPORTANTE:** 
- Use as credenciais do seu Supabase
- O Railway pode fornecer um PostgreSQL próprio, mas você pode continuar usando Supabase

### 📧 Configurações de Email

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app-gmail
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

**⚠️ IMPORTANTE:**
- Para Gmail, use uma "Senha de App" (não sua senha normal)
- Como criar: https://support.google.com/accounts/answer/185833

### 🌐 Configurações de API (Opcional)

```
DJANGO_API_URL=https://seu-app.railway.app
FASTAPI_URL=https://seu-app-fastapi.railway.app
```

---

## 🔧 Passo 2: Configurar Build e Deploy

### Build Command (Railway detecta automaticamente, mas você pode verificar):

```
pip install -r requirements.txt
```

### Start Command (já configurado no Procfile):

```
cd django_app && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 📝 Passo 3: Verificar Configurações

### 3.1 Verificar Procfile

O arquivo `Procfile` deve conter:
```
web: cd django_app && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

### 3.2 Verificar runtime.txt

O arquivo `runtime.txt` deve conter:
```
python-3.12.0
```

### 3.3 Verificar requirements.txt

Certifique-se de que contém:
- `gunicorn==21.2.0`
- `whitenoise==6.6.0`
- `psycopg2-binary==2.9.9` (para PostgreSQL/Supabase)

---

## 🚀 Passo 4: Fazer Deploy

1. **No Railway Dashboard:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha o repositório `pesquisa_nps`
   - Railway detectará automaticamente que é Django

2. **Configure as variáveis de ambiente** (Passo 1)

3. **Railway fará o deploy automaticamente!**

4. **Após o deploy:**
   - Railway fornecerá uma URL (ex: `https://seu-app.railway.app`)
   - Atualize `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` com a URL real

---

## 🔍 Passo 5: Criar Superusuário (Primeira vez)

Após o deploy, você precisa criar um superusuário para acessar o Django Admin:

### Opção A: Via Railway CLI

```bash
railway run python django_app/manage.py createsuperuser
```

### Opção B: Via Railway Dashboard

1. Vá em "Settings" → "Service"
2. Clique em "Shell"
3. Execute:
```bash
cd django_app
python manage.py createsuperuser
```

---

## ✅ Passo 6: Verificar se Está Funcionando

Acesse:
- **Admin:** `https://seu-app.railway.app/admin/`
- **API:** `https://seu-app.railway.app/api/`
- **Dashboard NPS:** `https://seu-app.railway.app/nps/dashboard/`

---

## 🔧 Troubleshooting

### Erro: "DisallowedHost"

**Solução:** Adicione o domínio do Railway em `ALLOWED_HOSTS`:
```
ALLOWED_HOSTS=*.railway.app,seu-app.railway.app
```

### Erro: "Static files not found"

**Solução:** Verifique se o `collectstatic` está no Procfile e se WhiteNoise está configurado.

### Erro: "Database connection failed"

**Solução:** 
- Verifique as credenciais do Supabase
- Certifique-se de que o IP do Railway está na whitelist do Supabase (se necessário)

### Erro: "Port already in use"

**Solução:** O Railway define `$PORT` automaticamente. Não defina manualmente.

---

## 📊 Monitoramento

No Railway Dashboard você pode:
- Ver logs em tempo real
- Ver métricas de uso
- Configurar domínio customizado
- Configurar variáveis de ambiente
- Ver histórico de deploys

---

## 🔄 Atualizações Futuras

Para atualizar o app após fazer mudanças:

1. Faça commit e push para o GitHub:
```bash
git add .
git commit -m "Sua mensagem"
git push
```

2. Railway detecta automaticamente e faz redeploy!

---

## 📚 Recursos

- **Railway Docs:** https://docs.railway.app
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/
- **WhiteNoise Docs:** http://whitenoise.evans.io/

---

**Status:** ✅ Pronto para deploy!

