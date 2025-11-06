# Guia de Configuração do Banco de Dados Supabase

Este guia explica como configurar o banco de dados PostgreSQL no Supabase para o projeto NPS Surveys.

## 📋 Pré-requisitos

1. Conta no Supabase (https://supabase.com)
2. Projeto criado no Supabase
3. Credenciais de conexão do projeto

## 🚀 Passo a Passo

### 1. Acessar o Supabase Dashboard

1. Acesse https://supabase.com
2. Faça login na sua conta
3. Selecione seu projeto (ou crie um novo)

### 2. Executar o Script SQL

1. No menu lateral, clique em **SQL Editor**
2. Clique em **New Query**
3. Abra o arquivo `database/supabase_schema.sql` deste projeto
4. Cole todo o conteúdo no editor SQL
5. Clique em **Run** (ou pressione `Ctrl+Enter`)

### 3. Verificar Criação das Tabelas

1. No menu lateral, clique em **Table Editor**
2. Você deve ver as seguintes tabelas criadas:
   - `surveys_survey`
   - `surveys_surveyinvitation`
   - `surveys_question`
   - `surveys_choice`
   - `surveys_surveyresponse`
   - `surveys_answer`
   - `surveys_npsresult`

### 4. Obter Credenciais de Conexão

1. No menu lateral, clique em **Settings** (⚙️)
2. Vá em **Database**
3. Role até a seção **Connection string**
4. Copie a **Connection string** (URI) ou anote:
   - Host
   - Database name
   - Port (geralmente 5432)
   - User
   - Password

### 5. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
# Supabase PostgreSQL Settings
DB_ENGINE=postgresql
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui

# Ou use a connection string completa
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

**⚠️ IMPORTANTE:**
- Substitua `[PASSWORD]` pela senha real do seu banco
- Substitua `xxxxxxxxxxxxx` pelo ID do seu projeto Supabase
- Mantenha a senha segura e nunca commite o arquivo `.env` no Git

### 6. Instalar Driver PostgreSQL para Django

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Instalar psycopg2 (driver PostgreSQL)
pip install psycopg2-binary
```

### 7. Configurar settings.py para Supabase

Edite `django_app/nps_admin/settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Database - Supabase PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

### 8. Executar Migrações do Django

```bash
cd django_app

# Criar migrações (se necessário)
python manage.py makemigrations

# Aplicar migrações
# NOTA: As tabelas já existem, então o Django vai detectar que já estão criadas
python manage.py migrate --run-syncdb

# Verificar status
python manage.py showmigrations
```

### 9. Criar Superusuário

```bash
cd django_app
python manage.py createsuperuser
```

Siga as instruções para criar um usuário admin.

### 10. Testar Conexão

Execute o script de teste:

```bash
python database/test_supabase_connection.py
```

## 🔍 Verificações

### Verificar Tabelas no Supabase

1. Acesse **Table Editor** no Supabase
2. Verifique se todas as 7 tabelas estão presentes
3. Clique em cada tabela para ver sua estrutura

### Verificar Índices

No SQL Editor, execute:

```sql
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
AND tablename LIKE 'surveys_%'
ORDER BY tablename, indexname;
```

### Verificar Foreign Keys

```sql
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_name LIKE 'surveys_%';
```

## ⚠️ Problemas Comuns

### Erro: "relation does not exist"

**Solução:** Execute o script SQL novamente ou verifique se está no schema correto.

### Erro: "permission denied"

**Solução:** Verifique as permissões do usuário no Supabase.

### Erro: "SSL connection required"

**Solução:** Adicione `'OPTIONS': {'sslmode': 'require'}` nas configurações do banco.

### Django não encontra as tabelas

**Solução:** 
1. Verifique se o nome do banco está correto
2. Execute `python manage.py migrate --run-syncdb`
3. Verifique se as tabelas existem no Supabase

## 📊 Estrutura das Tabelas

### surveys_survey
- Pesquisas NPS principais
- Campos: id, title, description, is_active, created_at, updated_at, etc.

### surveys_surveyinvitation
- Convites únicos por email
- Campos: id, survey_id, email, unique_token (UUID), is_used, expires_at

### surveys_question
- Perguntas de cada pesquisa
- Campos: id, survey_id, question_text, question_type, is_required, order

### surveys_choice
- Opções de múltipla escolha
- Campos: id, question_id, choice_text, value, order

### surveys_surveyresponse
- Respostas completas
- Campos: id, survey_id, invitation_id, respondent_id, submitted_at

### surveys_answer
- Respostas individuais
- Campos: id, response_id, question_id, answer_text, answer_value

### surveys_npsresult
- Resultados calculados
- Campos: id, survey_id, period_start, period_end, nps_score

## 🔐 Segurança

1. **Nunca commite** o arquivo `.env` com credenciais
2. Use **Row Level Security (RLS)** no Supabase se necessário
3. Configure **IP whitelist** no Supabase se aplicável
4. Use **variáveis de ambiente** em produção

## 📚 Recursos Adicionais

- [Documentação Supabase](https://supabase.com/docs)
- [Django PostgreSQL Setup](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

## ✅ Checklist Final

- [ ] Script SQL executado com sucesso
- [ ] Todas as 7 tabelas criadas
- [ ] Credenciais configuradas no `.env`
- [ ] `psycopg2-binary` instalado
- [ ] `settings.py` configurado para PostgreSQL
- [ ] Migrações do Django executadas
- [ ] Superusuário criado
- [ ] Teste de conexão bem-sucedido
- [ ] Tabelas verificadas no Supabase Dashboard

---

**Próximo Passo:** Após configurar o banco, continue com as correções críticas do projeto conforme `ESTADO_ATUAL_E_PROXIMOS_PASSOS.txt`
