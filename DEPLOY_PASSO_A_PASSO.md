# 🚀 Deploy Passo a Passo - Railway.app (Recomendado)

## 📋 Pré-requisitos

- ✅ Código no GitHub (ou GitLab)
- ✅ Conta no Railway.app (grátis)
- ✅ Banco Supabase configurado (já está!)
- ✅ Credenciais de email configuradas

## 🎯 Passo 1: Preparar o Código

### 1.1 Verificar arquivos necessários

Você já tem:
- ✅ `Procfile` - Comando de inicialização
- ✅ `runtime.txt` - Versão Python
- ✅ `requirements.txt` - Dependências (com gunicorn e whitenoise)

### 1.2 Commitar no GitHub

```bash
git add .
git commit -m "Preparado para deploy"
git push origin main
```

## 🎯 Passo 2: Criar Conta no Railway

1. Acesse: https://railway.app
2. Clique em "Login" ou "Get Started"
3. Escolha "Continue with GitHub"
4. Autorize Railway no GitHub

## 🎯 Passo 3: Criar Novo Projeto

1. No dashboard do Railway, clique em **"New Project"**
2. Escolha **"Deploy from GitHub repo"**
3. Selecione seu repositório `pesquisas_nps`
4. Railway detectará automaticamente que é Django

## 🎯 Passo 4: Configurar Variáveis de Ambiente

No Railway, vá em **"Variables"** e adicione:

```env
SECRET_KEY=sua-secret-key-muito-segura-aqui
DEBUG=False
ALLOWED_HOSTS=*.railway.app,seu-dominio.com
DB_HOST=aws-1-us-east-2.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.pzumhkxjasqntwujdztg
DB_PASSWORD=Pds2025@@
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app-gmail
DEFAULT_FROM_EMAIL=seu-email@gmail.com
PORT=8000
```

**⚠️ IMPORTANTE:**
- Substitua `SECRET_KEY` por uma chave segura (gere com: `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- Substitua as credenciais de email pelas suas
- `ALLOWED_HOSTS` será atualizado automaticamente com o domínio Railway

## 🎯 Passo 5: Configurar Build e Start

Railway detecta automaticamente, mas você pode verificar:

### Build Command:
```bash
pip install -r requirements.txt
```

### Start Command:
```bash
cd django_app && python manage.py migrate && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

(O Railway já usa o `Procfile` automaticamente!)

## 🎯 Passo 6: Fazer Deploy

1. Railway inicia o deploy automaticamente
2. Acompanhe os logs em tempo real
3. Aguarde o deploy terminar (2-5 minutos)

## 🎯 Passo 7: Criar Superusuário

Após o deploy, você precisa criar um superusuário:

1. No Railway, vá em **"Deployments"** > **"View Logs"**
2. Clique em **"Deploy Logs"** > **"Shell"**
3. Execute:
```bash
cd django_app
python manage.py createsuperuser
```

Ou via terminal local conectado ao Railway:
```bash
railway run python django_app/manage.py createsuperuser
```

## 🎯 Passo 8: Testar

1. Acesse: `https://seu-app.railway.app/admin`
2. Faça login com o superusuário criado
3. Teste criar uma pesquisa
4. Teste enviar convite por email
5. Teste responder pesquisa

## 🎯 Passo 9: Configurar Domínio Personalizado (Opcional)

1. No Railway, vá em **"Settings"** > **"Domains"**
2. Clique em **"Generate Domain"** ou adicione seu domínio
3. Configure DNS apontando para Railway

## ✅ Pronto!

Agora seu sistema está:
- ✅ Funcionando 24/7
- ✅ Sem depender da sua máquina
- ✅ Acessível de qualquer lugar
- ✅ Com HTTPS automático
- ✅ Com backup automático

---

## 🔄 Atualizações Futuras

### Deploy Automático:
- Faça `git push` no GitHub
- Railway detecta automaticamente
- Deploy automático em 2-5 minutos

### Deploy Manual:
- No Railway, vá em **"Deployments"**
- Clique em **"Redeploy"**

---

## 📊 Monitoramento

### Ver Logs:
- No Railway: **"Deployments"** > **"View Logs"**
- Logs em tempo real
- Filtrar por tipo de log

### Métricas:
- Uso de CPU
- Uso de memória
- Tráfego de rede
- Tempo de resposta

---

## 🆘 Resolução de Problemas

### Erro: "Module not found"
- Verifique se todas as dependências estão em `requirements.txt`
- Railway executa `pip install -r requirements.txt`

### Erro: "Database connection failed"
- Verifique variáveis de ambiente `DB_*`
- Verifique se Supabase permite conexões externas

### Erro: "Static files not found"
- Adicione `whitenoise` ao `requirements.txt` (já está!)
- Configure no `settings.py` (já está!)

### Erro: "Migration failed"
- Execute manualmente: `python manage.py migrate`
- Via Railway Shell

---

## 💰 Custos

### Railway Plano Grátis:
- ✅ 500 horas/mês grátis
- ✅ $5 crédito grátis/mês
- ✅ Suficiente para começar

### Se precisar mais:
- Plano Hobby: $5/mês
- Plano Pro: $20/mês

---

**Status**: ✅ Sistema pronto para deploy em produção! 🚀

