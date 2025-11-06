# ✅ Checklist de Deploy - NPS Surveys

## 📋 Antes de Fazer Deploy

### 1. Código Preparado
- [x] `Procfile` criado
- [x] `runtime.txt` criado
- [x] `requirements.txt` atualizado (gunicorn, whitenoise)
- [x] `settings.py` configurado (whitenoise, static files)
- [x] Código commitado no GitHub

### 2. Banco de Dados
- [x] Supabase PostgreSQL configurado
- [x] Credenciais de banco disponíveis
- [x] Migrações testadas localmente

### 3. Email
- [ ] Credenciais SMTP configuradas
- [ ] Senha de app Gmail criada (se usar Gmail)
- [ ] Teste de envio funcionando

### 4. Segurança
- [ ] `SECRET_KEY` seguro gerado
- [ ] `DEBUG=False` em produção
- [ ] `ALLOWED_HOSTS` configurado

## 🚀 Passos do Deploy (Railway)

### 1. Criar Conta
- [ ] Conta Railway criada
- [ ] Conectado ao GitHub
- [ ] Repositório selecionado

### 2. Configurar Variáveis
- [ ] `SECRET_KEY` adicionado
- [ ] `DEBUG=False` adicionado
- [ ] `ALLOWED_HOSTS` adicionado
- [ ] Variáveis de banco (`DB_*`) adicionadas
- [ ] Variáveis de email (`EMAIL_*`) adicionadas

### 3. Deploy
- [ ] Deploy iniciado
- [ ] Build concluído com sucesso
- [ ] Migrações aplicadas
- [ ] Aplicação iniciada

### 4. Pós-Deploy
- [ ] Superusuário criado
- [ ] Acesso ao admin funcionando
- [ ] Criar pesquisa testado
- [ ] Enviar convite testado
- [ ] Responder pesquisa testado
- [ ] Tracking de emails funcionando

## ✅ Testes em Produção

### Funcionalidades Básicas
- [ ] Login no admin funciona
- [ ] Criar pesquisa funciona
- [ ] Criar perguntas funciona
- [ ] Enviar convites funciona
- [ ] Email de convite chega
- [ ] Link de resposta funciona
- [ ] Formulário de resposta funciona
- [ ] Resposta é salva no banco
- [ ] Dashboard NPS funciona

### Tracking
- [ ] Pixel de abertura funciona
- [ ] Tracking de clique funciona
- [ ] Dashboard de tracking mostra dados

### Performance
- [ ] Páginas carregam rápido (< 2s)
- [ ] Sem erros nos logs
- [ ] Sem warnings críticos

## 🔒 Segurança

- [ ] HTTPS funcionando
- [ ] CSRF protegido
- [ ] Rate limiting ativo
- [ ] Senhas não expostas
- [ ] `.env` não commitado

## 📊 Monitoramento

- [ ] Logs acessíveis
- [ ] Métricas visíveis
- [ ] Alertas configurados (opcional)

## 🎯 Compartilhamento

- [ ] URL pública compartilhada com equipe
- [ ] Credenciais de acesso compartilhadas
- [ ] Documentação de uso compartilhada

---

## 📝 Notas

**Data do Deploy**: _______________

**Plataforma**: _______________

**URL**: _______________

**Superusuário**: _______________

**Observações**: _______________

---

**Status**: ✅ Checklist completo para deploy!

