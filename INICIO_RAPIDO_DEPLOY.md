# 🚀 Início Rápido - Deploy em Produção

## 🎯 Objetivo

Fazer o sistema funcionar **24/7 sem depender da sua máquina local**.

## ⚡ Solução Rápida (5 minutos)

### 1. Criar Conta Railway
👉 https://railway.app

### 2. Conectar GitHub
- Login com GitHub
- Selecionar repositório `pesquisas_nps`

### 3. Adicionar Variáveis de Ambiente
Copie do seu `.env` e adicione no Railway:
```
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DB_HOST=...
DB_PORT=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
EMAIL_HOST=...
EMAIL_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
DEFAULT_FROM_EMAIL=...
```

### 4. Deploy Automático!
Railway faz o resto automaticamente!

## 📚 Documentação Completa

Para instruções detalhadas, consulte:

1. **`RESUMO_DEPLOY.md`** - Visão geral rápida
2. **`DEPLOY_PASSO_A_PASSO.md`** - Guia passo a passo completo
3. **`GUIA_DEPLOY_PRODUCAO.md`** - Guia completo com todas as opções
4. **`COMPARACAO_PLATAFORMAS.md`** - Comparação de plataformas
5. **`CHECKLIST_DEPLOY.md`** - Checklist completo

## ✅ O que já está pronto

- ✅ `Procfile` - Comando de inicialização
- ✅ `runtime.txt` - Versão Python
- ✅ `requirements.txt` - Com gunicorn e whitenoise
- ✅ `settings.py` - Configurado para produção
- ✅ Banco Supabase - Já está na nuvem
- ✅ Código - Pronto para deploy

## 🎯 Próximo Passo

**Abra `DEPLOY_PASSO_A_PASSO.md` e siga as instruções!** 🚀

---

**Tempo estimado**: 20 minutos do início ao fim!

