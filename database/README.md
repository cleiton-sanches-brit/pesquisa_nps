# Scripts de Banco de Dados

Este diretório contém scripts e documentação para configuração do banco de dados.

## 📁 Arquivos

- **`supabase_schema.sql`** - Script SQL completo para criar todas as tabelas no Supabase PostgreSQL
- **`GUIA_SUPABASE.md`** - Guia passo a passo para configurar o Supabase
- **`test_supabase_connection.py`** - Script Python para testar conexão com Supabase
- **`init.sql`** - Script SQL original para SQL Server (mantido para referência)

## 🚀 Início Rápido

### 1. Executar Script SQL no Supabase

1. Acesse seu projeto no Supabase
2. Vá em **SQL Editor**
3. Cole o conteúdo de `supabase_schema.sql`
4. Execute o script

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha
```

### 3. Testar Conexão

```bash
python database/test_supabase_connection.py
```

### 4. Configurar Django

Copie o conteúdo de `settings_supabase.py` para `settings.py` ou ajuste conforme necessário.

## 📚 Documentação Completa

Consulte `GUIA_SUPABASE.md` para instruções detalhadas.

## ⚠️ Notas Importantes

- As tabelas do Django (auth_user, etc.) serão criadas automaticamente via migrações
- O script SQL cria apenas as tabelas do app `surveys`
- Certifique-se de ter `psycopg2-binary` instalado: `pip install psycopg2-binary`
- SSL é obrigatório para conexões Supabase
