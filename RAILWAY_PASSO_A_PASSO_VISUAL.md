# 🚀 Guia Visual: Configurar Projeto no Railway

## 📋 Passo 1: Criar Novo Projeto no Railway

### 1.1 Acessar o Dashboard
1. Acesse: https://railway.app
2. Faça login com sua conta GitHub
3. Você verá o **Dashboard** com seu workspace

### 1.2 Criar Novo Projeto
1. No canto superior direito, clique no botão **"+ New Project"** (ou **"+ New"**)
2. Você verá 3 opções:
   - **Deploy from GitHub repo** ← **ESCOLHA ESTA**
   - **Empty Project**
   - **Deploy a Template**

### 1.3 Conectar Repositório GitHub
1. Clique em **"Deploy from GitHub repo"**
2. Se for a primeira vez, Railway pedirá permissão para acessar seus repositórios
3. Clique em **"Authorize Railway"** ou **"Install Railway"**
4. Selecione o repositório: **`cleiton-sanches-brit/pesquisa_nps`**
5. Clique em **"Deploy"** ou **"Add"**

---

## 📦 Passo 2: Railway Detecta e Configura Automaticamente

Após conectar o repositório:
- Railway detecta que é um projeto Django
- Inicia o build automaticamente
- Você verá os logs do build em tempo real

**⚠️ O primeiro deploy pode falhar** porque ainda não configuramos as variáveis de ambiente. Isso é normal!

---

## ⚙️ Passo 3: Encontrar e Configurar Variáveis de Ambiente

### 3.1 Acessar as Configurações do Serviço

**Opção A: Pelo Menu Lateral**
1. No dashboard, você verá seu projeto listado
2. Clique no **nome do projeto** (ou no card do serviço)
3. Você verá uma página com abas no topo:
   - **Deployments** (padrão)
   - **Settings** ← **CLIQUE AQUI**
   - **Metrics**
   - **Logs**

**Opção B: Pelo Menu de Três Pontos**
1. No card do serviço, clique nos **três pontinhos** (⋯) no canto superior direito
2. Selecione **"Settings"**

### 3.2 Encontrar a Seção de Variáveis

Na página **Settings**, você verá várias seções:

1. **Service Name** - Nome do serviço
2. **Source** - Repositório conectado
3. **Variables** ← **ESTA É A SEÇÃO QUE VOCÊ PRECISA!**
4. **Build & Deploy Settings**
5. **Networking**
6. **Health Checks**

### 3.3 Adicionar Variáveis

Na seção **Variables**:

1. Você verá um botão **"+ New Variable"** ou **"Add Variable"**
2. Clique nele
3. Adicione cada variável uma por uma:

**Exemplo:**
- **Name:** `SECRET_KEY`
- **Value:** `sua-chave-secreta-aqui`
- Clique em **"Add"** ou **"Save"**

4. Repita para todas as variáveis necessárias

---

## 📝 Passo 4: Lista Completa de Variáveis

Adicione estas variáveis na seção **Variables**:

### Configurações Django
```
SECRET_KEY = (gere uma chave segura)
DEBUG = False
ALLOWED_HOSTS = *.railway.app
CSRF_TRUSTED_ORIGINS = https://*.railway.app
```

### Banco de Dados (Supabase)
```
DB_HOST = aws-1-us-east-2.pooler.supabase.com
DB_PORT = 6543
DB_NAME = postgres
DB_USER = postgres.pzumhkxjasqntwujdztg
DB_PASSWORD = Pds2025@@
```

### Email
```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = seu-email@gmail.com
EMAIL_HOST_PASSWORD = sua-senha-de-app
DEFAULT_FROM_EMAIL = seu-email@gmail.com
```

---

## 🔄 Passo 5: Fazer Redeploy

Após adicionar todas as variáveis:

1. Vá para a aba **"Deployments"**
2. Clique nos **três pontinhos** (⋯) no último deploy
3. Selecione **"Redeploy"** ou **"Deploy"**
4. Ou simplesmente faça um novo commit no GitHub (Railway detecta automaticamente)

---

## 🔍 Passo 6: Verificar Logs

Durante o deploy:

1. Clique na aba **"Logs"**
2. Você verá os logs em tempo real
3. Procure por erros (em vermelho)

**Logs importantes:**
- `Collecting static files...` ✅
- `Running migrations...` ✅
- `Starting gunicorn...` ✅

---

## 🌐 Passo 7: Obter URL do App

Após o deploy bem-sucedido:

1. Vá para a aba **"Settings"**
2. Role até a seção **"Networking"** ou **"Domains"**
3. Você verá uma URL como: `https://seu-app.railway.app`
4. Copie esta URL

### Atualizar ALLOWED_HOSTS com a URL Real

1. Volte para **Variables**
2. Edite `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS = *.railway.app,seu-app.railway.app
   ```
3. Edite `CSRF_TRUSTED_ORIGINS`:
   ```
   CSRF_TRUSTED_ORIGINS = https://*.railway.app,https://seu-app.railway.app
   ```
4. Substitua `seu-app.railway.app` pela URL real que o Railway forneceu

---

## 🆘 Problemas Comuns

### "Não vejo o botão New Project"
- Certifique-se de estar logado
- Verifique se está no workspace correto
- Tente atualizar a página (F5)

### "Não encontro a seção Variables"
- Certifique-se de ter clicado no **serviço/projeto** (não apenas no workspace)
- Procure pela aba **"Settings"** no topo da página
- A seção Variables fica no meio da página Settings

### "O repositório não aparece na lista"
- Verifique se autorizou o Railway a acessar seus repositórios
- Vá em: https://github.com/settings/installations
- Verifique se Railway está instalado e tem permissão

### "Build falha"
- Verifique os logs na aba **"Logs"**
- Certifique-se de que todas as variáveis foram adicionadas
- Verifique se o `Procfile` está correto

---

## 📸 Estrutura Visual do Railway Dashboard

```
┌─────────────────────────────────────────┐
│  Railway Dashboard                      │
│  ┌───────────────────────────────────┐ │
│  │  Workspace: seu-workspace         │ │
│  │                                   │ │
│  │  [+ New Project]  ← Clique aqui  │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Projeto: pesquisa_nps      │ │ │
│  │  │  [Deployments] [Settings]   │ │ │
│  │  │                             │ │ │
│  │  │  Settings:                 │ │ │
│  │  │  ┌───────────────────────┐ │ │ │
│  │  │  │ Variables             │ │ │ │
│  │  │  │ [+ New Variable]  ←───┼─┼─┘ │
│  │  │  └───────────────────────┘ │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## ✅ Checklist Final

- [ ] Projeto criado no Railway
- [ ] Repositório GitHub conectado
- [ ] Todas as variáveis de ambiente adicionadas
- [ ] Deploy realizado com sucesso
- [ ] URL do app obtida
- [ ] ALLOWED_HOSTS atualizado com a URL real
- [ ] App acessível via URL do Railway

---

**Precisa de mais ajuda?** Me diga em qual passo você está travado e eu te ajudo! 🚀

