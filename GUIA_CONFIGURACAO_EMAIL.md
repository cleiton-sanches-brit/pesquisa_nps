# Guia de Configuração de Email - NPS Surveys

## 📧 Configuração de Email para Envio de Convites

Este guia explica como configurar o envio de emails para o sistema de convites de pesquisas NPS.

## ✅ O que já está implementado

- ✅ Configurações de SMTP no `settings.py`
- ✅ Template de email HTML (`email_invitation.html`)
- ✅ Sistema de tracking de emails (abertura e cliques)
- ✅ Código de envio de emails nas views

## 🔧 O que falta configurar

**Apenas as credenciais de email no arquivo `.env`**

## 📋 Passo a Passo

### 1. Escolher o Provedor de Email

Você pode usar qualquer provedor SMTP. Os mais comuns são:

#### Gmail (Recomendado para testes)
- **Host**: `smtp.gmail.com`
- **Porta**: `587` (TLS) ou `465` (SSL)
- **TLS**: `True`

#### Outlook/Hotmail
- **Host**: `smtp-mail.outlook.com`
- **Porta**: `587`
- **TLS**: `True`

#### Outros provedores
- Verifique a documentação do seu provedor para as configurações SMTP

### 2. Configurar Gmail (Exemplo)

#### Para Gmail, você precisa criar uma "Senha de App":

1. Acesse: https://myaccount.google.com/apppasswords
2. Faça login na sua conta Google
3. Selecione "App" e "Outro (Nome personalizado)"
4. Digite um nome (ex: "NPS Surveys")
5. Clique em "Gerar"
6. Copie a senha gerada (16 caracteres)

**⚠️ IMPORTANTE**: Não use sua senha normal do Gmail! Use uma senha de app.

### 3. Configurar no arquivo `.env`

Abra o arquivo `.env` na raiz do projeto e adicione:

```env
# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app-gerada
DEFAULT_FROM_EMAIL=seu-email@gmail.com
```

**Exemplo completo:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=meuemail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=meuemail@gmail.com
```

### 4. Testar o Envio de Email

Use o script de teste fornecido:

```bash
python testar_envio_email.py
```

Ou execute via PowerShell:
```powershell
.\venv\Scripts\python.exe testar_envio_email.py
```

## 🔒 Segurança

### ⚠️ NUNCA faça:
- ❌ Commitar o arquivo `.env` no Git
- ❌ Compartilhar senhas de email
- ❌ Usar senha normal do Gmail (use senha de app)

### ✅ SEMPRE faça:
- ✅ Manter o `.env` no `.gitignore`
- ✅ Usar senhas de app para Gmail
- ✅ Testar em ambiente de desenvolvimento primeiro

## 📝 Configurações por Provedor

### Gmail
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app
```

### Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@outlook.com
EMAIL_HOST_PASSWORD=sua-senha
```

### Yahoo
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@yahoo.com
EMAIL_HOST_PASSWORD=sua-senha
```

### Servidor SMTP Corporativo
```env
EMAIL_HOST=smtp.empresa.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=usuario@empresa.com
EMAIL_HOST_PASSWORD=senha-corporativa
```

## 🧪 Teste de Envio

Após configurar, teste o envio:

1. **Via Script de Teste** (recomendado):
   ```bash
   python testar_envio_email.py
   ```

2. **Via Django Admin**:
   - Acesse http://localhost:8000/admin/
   - Vá em "Surveys" > Selecione uma pesquisa
   - Clique em "Enviar Convites"
   - Digite um email de teste
   - Clique em "Enviar"

3. **Verificar Logs**:
   - Se houver erro, verifique o console do Django
   - Erros comuns:
     - Credenciais incorretas
     - Senha de app não configurada (Gmail)
     - Firewall bloqueando conexão SMTP

## 🐛 Resolução de Problemas

### Erro: "Authentication failed"
- ✅ Verifique se `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` estão corretos
- ✅ Para Gmail, certifique-se de usar senha de app, não senha normal

### Erro: "Connection refused"
- ✅ Verifique se a porta está correta (587 para TLS, 465 para SSL)
- ✅ Verifique se o firewall não está bloqueando
- ✅ Teste a conectividade: `telnet smtp.gmail.com 587`

### Erro: "TLS/SSL required"
- ✅ Certifique-se de que `EMAIL_USE_TLS=True` para porta 587
- ✅ Ou use `EMAIL_USE_SSL=True` para porta 465

### Email não chega
- ✅ Verifique a pasta de spam
- ✅ Verifique se o email de destino está correto
- ✅ Verifique os logs do Django para erros

## 📊 Monitoramento

Após configurar, você pode monitorar:
- ✅ Emails enviados (via Django Admin)
- ✅ Tracking de abertura (quando email foi aberto)
- ✅ Tracking de cliques (quando link foi clicado)
- ✅ Status dos convites (enviado, aberto, clicado, respondido)

## 📚 Referências

- [Django Email Documentation](https://docs.djangoproject.com/en/4.2/topics/email/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [SMTP Settings by Provider](https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html)

---

**Status**: ✅ Configurações prontas - Apenas falta adicionar credenciais no `.env`

