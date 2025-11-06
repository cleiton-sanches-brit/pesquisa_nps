# 🚀 Guia de Deploy em Produção - NPS Surveys

## 📋 Objetivo

Fazer o sistema funcionar 24/7 sem depender da sua máquina local estar ligada.

## ✅ O que já está pronto

- ✅ **Banco de dados**: Supabase PostgreSQL (já está na nuvem)
- ✅ **Código**: Pronto para deploy
- ✅ **Configurações**: Separadas por ambiente (.env)

## 🎯 Opções de Hospedagem

### 🥇 **OPÇÃO 1: Railway.app (RECOMENDADO - Mais Fácil)**

**Vantagens:**
- ✅ Grátis para começar (500 horas/mês)
- ✅ Deploy automático via GitHub
- ✅ Configuração muito simples
- ✅ Suporta PostgreSQL (usa Supabase)
- ✅ HTTPS automático
- ✅ Sem configuração de servidor

**Passos:**
1. Criar conta em: https://railway.app
2. Conectar repositório GitHub
3. Railway detecta Django automaticamente
4. Adicionar variáveis de ambiente (.env)
5. Deploy automático!

**Custo:** Grátis (plano básico suficiente para começar)

---

### 🥈 **OPÇÃO 2: Render.com**

**Vantagens:**
- ✅ Grátis para começar
- ✅ Fácil configuração
- ✅ Deploy automático
- ✅ HTTPS automático

**Passos:**
1. Criar conta em: https://render.com
2. Conectar GitHub
3. Criar Web Service (Django)
4. Configurar variáveis de ambiente
5. Deploy!

**Custo:** Grátis (pode hibernar após 15min sem uso)

---

### 🥉 **OPÇÃO 3: Heroku**

**Vantagens:**
- ✅ Popular e confiável
- ✅ Muitos recursos
- ✅ Fácil deploy

**Desvantagens:**
- ❌ Não tem mais plano grátis
- ❌ Precisa cartão de crédito

**Custo:** ~$7/mês (plano básico)

---

### 🏆 **OPÇÃO 4: DigitalOcean App Platform**

**Vantagens:**
- ✅ Muito confiável
- ✅ Boa performance
- ✅ Escalável

**Custo:** ~$5/mês (plano básico)

---

### 🔧 **OPÇÃO 5: VPS (DigitalOcean, Linode, AWS EC2)**

**Vantagens:**
- ✅ Controle total
- ✅ Mais barato a longo prazo
- ✅ Personalizável

**Desvantagens:**
- ❌ Requer conhecimento técnico
- ❌ Você gerencia o servidor

**Custo:** ~$5-10/mês

---

## 📊 Comparação Rápida

| Opção | Dificuldade | Custo | Recomendado para |
|-------|-------------|-------|------------------|
| **Railway** | ⭐ Fácil | Grátis | ✅ Iniciantes |
| **Render** | ⭐ Fácil | Grátis | ✅ Iniciantes |
| **Heroku** | ⭐⭐ Médio | $7/mês | Intermediário |
| **DigitalOcean** | ⭐⭐ Médio | $5/mês | Intermediário |
| **VPS** | ⭐⭐⭐ Difícil | $5-10/mês | Avançado |

## 🎯 RECOMENDAÇÃO: Railway.app

### Por quê?

1. **Mais fácil**: Configuração em 5 minutos
2. **Grátis**: Plano básico suficiente
3. **Automático**: Deploy direto do GitHub
4. **Sem servidor**: Não precisa gerenciar nada
5. **Sempre online**: Não hiberna como Render

### Passo a Passo - Railway

#### 1. Preparar o Projeto

Criar arquivo `Procfile` na raiz:
```
web: cd django_app && python manage.py migrate && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

Criar `runtime.txt`:
```
python-3.12.0
```

#### 2. Criar Conta Railway

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Escolha "Deploy from GitHub repo"
4. Autorize Railway no GitHub
5. Selecione seu repositório

#### 3. Configurar Variáveis de Ambiente

No Railway, adicione todas as variáveis do `.env`:

```
SECRET_KEY=sua-secret-key
DEBUG=False
ALLOWED_HOSTS=seu-app.railway.app,seu-dominio.com
DB_HOST=aws-1-us-east-2.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.pzumhkxjasqntwujdztg
DB_PASSWORD=Pds2025@@
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

#### 4. Configurar Build

Railway detecta automaticamente Django, mas você pode especificar:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
cd django_app && python manage.py migrate && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT
```

#### 5. Deploy!

Railway faz deploy automático a cada push no GitHub!

---

## 📝 Checklist de Deploy

### Antes de Fazer Deploy:

- [ ] Código no GitHub/GitLab
- [ ] Banco de dados Supabase configurado
- [ ] Credenciais de email configuradas
- [ ] `ALLOWED_HOSTS` atualizado
- [ ] `DEBUG=False` em produção
- [ ] `SECRET_KEY` seguro gerado
- [ ] Migrações aplicadas
- [ ] Superusuário criado

### Arquivos Necessários:

- [ ] `Procfile` (para Railway/Render)
- [ ] `runtime.txt` (versão Python)
- [ ] `requirements.txt` (atualizado)
- [ ] `.gitignore` (não commitar .env)

### Configurações de Produção:

- [ ] Variáveis de ambiente configuradas
- [ ] Email SMTP configurado
- [ ] CORS configurado (se necessário)
- [ ] Static files configurados
- [ ] SSL/HTTPS ativado

---

## 🔧 Configurações Adicionais

### 1. Static Files (CSS, JS, Imagens)

Para Railway/Render, adicione ao `settings.py`:

```python
# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Em produção, usar whitenoise
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicionar
    # ... outros middlewares
]
```

E no `requirements.txt`:
```
whitenoise==6.6.0
```

### 2. Gunicorn (Servidor WSGI)

Adicionar ao `requirements.txt`:
```
gunicorn==21.2.0
```

### 3. Domínio Personalizado

No Railway/Render:
1. Vá em "Settings" > "Domains"
2. Adicione seu domínio
3. Configure DNS apontando para o servidor

---

## 🧪 Testar em Produção

### Após Deploy:

1. Acesse: `https://seu-app.railway.app/admin`
2. Faça login com superusuário
3. Teste criar uma pesquisa
4. Teste enviar convite por email
5. Teste responder pesquisa

---

## 📊 Monitoramento

### Railway Dashboard:
- Ver logs em tempo real
- Ver uso de recursos
- Ver métricas de performance

### Alertas:
- Configurar email para erros
- Monitorar uso de recursos

---

## 🔄 Atualizações

### Deploy Automático:
- Push no GitHub → Deploy automático
- Ou deploy manual pelo dashboard

### Migrações:
- Railway executa automaticamente no start
- Ou rodar manualmente: `python manage.py migrate`

---

## 💰 Custos Estimados

### Railway (Recomendado):
- **Início**: Grátis (500 horas/mês)
- **Uso moderado**: Grátis
- **Uso intenso**: ~$5-10/mês

### Render:
- **Início**: Grátis (hiberna após 15min)
- **Sempre online**: ~$7/mês

### Heroku:
- **Plano básico**: ~$7/mês

---

## 🆘 Suporte

### Problemas Comuns:

1. **Erro de migração**: Executar manualmente
2. **Static files não aparecem**: Configurar whitenoise
3. **Email não funciona**: Verificar credenciais SMTP
4. **Banco não conecta**: Verificar variáveis de ambiente

---

## ✅ Próximos Passos

1. **Escolher plataforma** (Recomendo Railway)
2. **Criar conta**
3. **Conectar GitHub**
4. **Configurar variáveis**
5. **Fazer deploy**
6. **Testar**
7. **Compartilhar URL com equipe!**

---

**Status**: ✅ Guia completo de deploy criado!

**Recomendação Final**: Use **Railway.app** para começar - é a opção mais fácil e rápida! 🚀

