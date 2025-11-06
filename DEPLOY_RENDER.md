# 🚀 Guia de Deploy no Render.com (GRATUITO)

## ✅ Por que Render.com?

- ✅ **100% Gratuito** para começar
- ✅ Deploy automático do GitHub
- ✅ Suporta PostgreSQL (pode usar Supabase)
- ✅ HTTPS automático
- ✅ Interface web fácil
- ✅ Não requer cartão de crédito
- ⚠️ Pode hibernar após 15min sem uso (mas acorda rápido)

---

## 📋 Passo 1: Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Escolha **"Sign up with GitHub"**
4. Autorize Render a acessar seus repositórios

---

## 🚀 Passo 2: Criar Web Service

### 2.1 Iniciar Deploy

1. No dashboard do Render, clique em **"+ New"**
2. Selecione **"Web Service"**
3. Conecte seu repositório GitHub:
   - Clique em **"Connect account"** (se primeira vez)
   - Selecione o repositório: **`cleiton-sanches-brit/pesquisa_nps`**
   - Clique em **"Connect"**

### 2.2 Configurar Serviço

Preencha os campos:

**Name:**
```
pesquisa-nps
```

**Region:**
```
Oregon (US West) - ou mais próximo de você
```

**Branch:**
```
main
```

**Root Directory:**
```
(deixe vazio - está na raiz)
```

**Runtime:**
```
Python 3
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
cd django_app && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

**Instance Type:**
```
Free (512 MB RAM)
```

### 2.3 Configurar Variáveis de Ambiente

Role a página até **"Environment Variables"** e adicione:

#### Configurações Django
```
SECRET_KEY = (gere uma chave segura)
DEBUG = False
ALLOWED_HOSTS = *.onrender.com
CSRF_TRUSTED_ORIGINS = https://*.onrender.com
```

#### Banco de Dados (Supabase)
```
DB_HOST = aws-1-us-east-2.pooler.supabase.com
DB_PORT = 6543
DB_NAME = postgres
DB_USER = postgres.pzumhkxjasqntwujdztg
DB_PASSWORD = Pds2025@@
```

#### Email
```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = seu-email@gmail.com
EMAIL_HOST_PASSWORD = sua-senha-de-app
DEFAULT_FROM_EMAIL = seu-email@gmail.com
```

### 2.4 Criar Serviço

1. Clique em **"Create Web Service"**
2. Render começará o build automaticamente
3. Você verá os logs em tempo real

---

## ⏱️ Passo 3: Aguardar Deploy

O primeiro deploy pode levar 5-10 minutos:
- ✅ Instalando dependências
- ✅ Executando migrações
- ✅ Coletando arquivos estáticos
- ✅ Iniciando servidor

**Você verá os logs em tempo real!**

---

## 🌐 Passo 4: Obter URL e Atualizar Configurações

### 4.1 Obter URL

Após o deploy bem-sucedido:
1. Render fornecerá uma URL: `https://pesquisa-nps.onrender.com`
2. Copie esta URL

### 4.2 Atualizar ALLOWED_HOSTS

1. Vá em **"Environment"** (aba do serviço)
2. Edite `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS = *.onrender.com,pesquisa-nps.onrender.com
   ```
3. Edite `CSRF_TRUSTED_ORIGINS`:
   ```
   CSRF_TRUSTED_ORIGINS = https://*.onrender.com,https://pesquisa-nps.onrender.com
   ```
4. Render fará redeploy automaticamente

---

## 👤 Passo 5: Criar Superusuário

### 5.1 Via Render Shell

1. No dashboard do serviço, clique em **"Shell"** (no menu lateral)
2. Execute:
   ```bash
   cd django_app
   python manage.py createsuperuser
   ```
3. Preencha os dados do superusuário

### 5.2 Via Terminal Local (SSH)

Se Render permitir SSH:
```bash
render ssh pesquisa-nps
cd django_app
python manage.py createsuperuser
```

---

## ✅ Passo 6: Verificar se Está Funcionando

Acesse:
- **Admin:** `https://pesquisa-nps.onrender.com/admin/`
- **API:** `https://pesquisa-nps.onrender.com/api/`
- **Dashboard NPS:** `https://pesquisa-nps.onrender.com/nps/dashboard/`

---

## 🔄 Passo 7: Atualizações Futuras

Render detecta automaticamente novos commits no GitHub:

1. Faça commit e push:
   ```bash
   git add .
   git commit -m "Sua mensagem"
   git push
   ```

2. Render detecta e faz redeploy automaticamente!

---

## ⚙️ Configurações Adicionais

### Auto-Deploy

Por padrão, Render faz deploy automático. Você pode:
- Desabilitar em **"Settings"** → **"Auto-Deploy"**
- Fazer deploy manual clicando em **"Manual Deploy"**

### Domínio Personalizado

1. Vá em **"Settings"** → **"Custom Domains"**
2. Adicione seu domínio
3. Configure DNS apontando para Render

### Health Checks

Render verifica automaticamente se o app está rodando:
- Acessa `/` periodicamente
- Se falhar, Render reinicia o serviço

---

## 🔍 Troubleshooting

### "Build failed"

**Verifique os logs:**
1. Clique em **"Logs"** no dashboard
2. Procure por erros (em vermelho)
3. Verifique se todas as variáveis foram adicionadas

### "Application error"

**Possíveis causas:**
- Variáveis de ambiente faltando
- Erro no banco de dados
- Erro no settings.py

**Solução:**
1. Verifique os logs
2. Confirme todas as variáveis
3. Teste conexão com banco

### "Static files not found"

**Solução:**
- Verifique se `collectstatic` está no Start Command
- Confirme que WhiteNoise está instalado

### "App hibernado"

**No plano gratuito:**
- App pode hibernar após 15min sem uso
- Primeira requisição pode demorar ~30s para "acordar"
- Isso é normal no plano gratuito

**Para evitar hibernação:**
- Upgrade para plano pago
- Ou use serviço de "ping" para manter ativo

---

## 📊 Comparação: Render vs Railway

| Recurso | Render (Gratuito) | Railway (Pago) |
|---------|-------------------|----------------|
| Custo | ✅ Gratuito | ❌ Pago |
| Deploy Auto | ✅ Sim | ✅ Sim |
| PostgreSQL | ✅ Sim | ✅ Sim |
| HTTPS | ✅ Sim | ✅ Sim |
| Hibernação | ⚠️ Sim (15min) | ❌ Não |
| Interface | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## ✅ Checklist Final

- [ ] Conta Render criada
- [ ] Repositório GitHub conectado
- [ ] Web Service criado
- [ ] Todas as variáveis de ambiente adicionadas
- [ ] Deploy realizado com sucesso
- [ ] URL obtida
- [ ] ALLOWED_HOSTS atualizado
- [ ] Superusuário criado
- [ ] App acessível e funcionando

---

## 🎯 Próximos Passos

1. Teste todas as funcionalidades
2. Configure domínio personalizado (opcional)
3. Configure monitoramento (opcional)
4. Faça backup regular do banco de dados

---

**Status:** ✅ Render.com é a melhor opção gratuita! 🚀

