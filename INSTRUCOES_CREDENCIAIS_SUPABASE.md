# 📋 Instruções para Configurar Credenciais do Supabase

## ⚠️ Importante: Você Precisa Fornecer as Credenciais

Sim, você está certo! Para configurar completamente o projeto, precisamos das credenciais do Supabase. Mas há **duas partes** no processo:

---

## 🎯 PARTE 1: Criar Tabelas (NÃO precisa de credenciais externas)

Esta parte você faz **direto no Supabase Dashboard**:

1. ✅ Acesse https://supabase.com/dashboard
2. ✅ Selecione seu projeto
3. ✅ Vá em **SQL Editor** (menu lateral)
4. ✅ Clique em **New Query**
5. ✅ Abra o arquivo `database/supabase_schema.sql` deste projeto
6. ✅ Cole todo o conteúdo no editor
7. ✅ Clique em **Run** (ou `Ctrl+Enter`)

**Isso cria todas as tabelas!** Não precisa de credenciais externas para isso.

---

## 🔑 PARTE 2: Configurar Conexão Django (PRECISA de credenciais)

Para conectar o Django ao Supabase, você precisa fornecer:

### Onde Encontrar as Credenciais:

1. No Supabase Dashboard, vá em **Settings** (⚙️) no menu lateral
2. Clique em **Database**
3. Role até a seção **Connection string**
4. Você verá:
   - **Host**: `db.xxxxxxxxxxxxx.supabase.co`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres`
   - **Password**: (clique em "Reset database password" se não souber)

### Como Fornecer as Credenciais:

**Opção 1: Editar .env manualmente**

Edite o arquivo `.env` na raiz do projeto e adicione/atualize:

```env
# Supabase PostgreSQL Settings
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

**Opção 2: Usar o script de configuração**

1. Execute: `.\configurar_supabase.ps1`
2. O script vai pedir para você editar o `.env`
3. Após editar, o script continuará automaticamente

**Opção 3: Me fornecer as credenciais**

Você pode me informar:
- Host (ex: `db.abc123.supabase.co`)
- Port (geralmente `5432`)
- Database (geralmente `postgres`)
- User (geralmente `postgres`)
- Password (sua senha do banco)

⚠️ **IMPORTANTE**: Se você me fornecer as credenciais aqui, **não as compartilhe publicamente** depois. Use apenas para configuração inicial.

---

## 📝 Checklist de Configuração

### ✅ Fazer Agora (sem credenciais):
- [ ] Executar script SQL no Supabase Dashboard
- [ ] Verificar que as 7 tabelas foram criadas

### 🔑 Fazer Depois (com credenciais):
- [ ] Obter credenciais no Supabase Dashboard
- [ ] Configurar arquivo `.env`
- [ ] Instalar `psycopg2-binary`: `pip install psycopg2-binary`
- [ ] Executar script de teste: `python database/test_supabase_connection.py`
- [ ] Configurar Django para usar Supabase
- [ ] Executar migrações do Django

---

## 🚀 Quando Você Tiver as Credenciais

Após obter as credenciais, você pode:

1. **Me fornecer aqui** e eu configuro tudo para você
2. **Ou seguir o guia** `database/GUIA_SUPABASE.md` passo a passo
3. **Ou executar** o script `configurar_supabase.ps1`

---

## 🔒 Segurança

⚠️ **NUNCA commite o arquivo `.env` no Git!**

O arquivo `.env` já está no `.gitignore` para proteção.

---

## ❓ Próximo Passo

**O que você prefere?**

1. 🎯 **Executar o script SQL primeiro** (não precisa de credenciais - faça no Supabase Dashboard)
2. 🔑 **Me fornecer as credenciais** e eu configuro tudo
3. 📖 **Seguir o guia passo a passo** (`database/GUIA_SUPABASE.md`)

Me avise qual opção você prefere! 😊
