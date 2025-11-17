# 📊 Guia de Configuração para Power BI

Este guia explica como configurar as tabelas e views para consumo no Power BI.

## 🎯 Estrutura para Power BI

O sistema foi configurado com **3 tabelas principais** conectadas por **EMAIL** como chave:

### 1️⃣ **Tabela de Respostas** (`vw_powerbi_respostas`)
- **Chave**: `email_respondente`
- **Conteúdo**: Dados das respostas recebidas
- **Campos principais**:
  - Email do respondente
  - Data da resposta
  - Resposta NPS
  - Classificação (Promotor/Neutro/Detrator)
  - Informações da pesquisa

### 2️⃣ **Tabela de Envios** (`vw_powerbi_envios`)
- **Chave**: `email_destinatario`
- **Conteúdo**: Dados de envio de convites
- **Campos principais**:
  - Email do destinatário
  - Data de envio
  - Status do convite (Válido/Utilizado/Expirado)
  - Se foi respondido

### 3️⃣ **Tabela de Cadastro** (`vw_powerbi_respondentes`)
- **Chave**: `email_usuario`
- **Conteúdo**: Cadastro de possíveis respondentes
- **Campos principais**:
  - Email do usuário
  - Nome da conta
  - Nome do usuário
  - Status do usuário
  - Taxa de resposta

## 🚀 Passo a Passo

### 1. Criar Tabela de Cadastro

Execute o script SQL no Supabase:

```sql
-- Executar database/tabela_respondents.sql
```

Ou via Supabase Dashboard:
1. Acesse **SQL Editor**
2. Abra `database/tabela_respondents.sql`
3. Execute o script

### 2. Criar Views para Power BI

Execute o script SQL no Supabase:

```sql
-- Executar database/powerbi_views.sql
```

### 3. Criar Migração Django (Opcional)

Se quiser gerenciar via Django Admin:

```bash
cd django_app
python manage.py makemigrations
python manage.py migrate
```

### 4. Conectar Power BI

#### Opção A: Via Supabase (Recomendado)

1. Abra Power BI Desktop
2. **Obter Dados** > **Banco de dados** > **PostgreSQL**
3. Preencha:
   - **Servidor**: `aws-1-us-east-2.pooler.supabase.com`
   - **Porta**: `6543`
   - **Banco de dados**: `postgres`
   - **Modo de dados**: Importar ou DirectQuery
4. Autentique com:
   - **Usuário**: `postgres.pzumhkxjasqntwujdztg`
   - **Senha**: `Pds2025@@`

#### Opção B: Via Connection String

```
postgresql://postgres.pzumhkxjasqntwujdztg:Pds2025@@@aws-1-us-east-2.pooler.supabase.com:6543/postgres
```

### 5. Selecionar Views

No Power BI, selecione as views:

- ✅ `vw_powerbi_respostas`
- ✅ `vw_powerbi_envios`
- ✅ `vw_powerbi_respondentes`
- ✅ `vw_powerbi_consolidado` (opcional - view consolidada)

### 6. Criar Relacionamentos

No Power BI, crie relacionamentos usando **EMAIL**:

```
vw_powerbi_respondentes[email_usuario] 
  → vw_powerbi_envios[email_destinatario]
  → vw_powerbi_respostas[email_respondente]
```

## 📋 Campos Disponíveis

### vw_powerbi_respostas
- `email_respondente` ⭐ (chave)
- `resposta_id`
- `data_resposta`
- `resposta_nps`
- `classificacao_nps`
- `titulo_pesquisa`
- `total_perguntas_respondidas`

### vw_powerbi_envios
- `email_destinatario` ⭐ (chave)
- `envio_id`
- `data_envio`
- `status_convite`
- `foi_respondido`
- `dias_desde_envio`

### vw_powerbi_respondentes
- `email_usuario` ⭐ (chave)
- `nome_conta`
- `nome_usuario`
- `status_usuario`
- `taxa_resposta_percentual`
- `total_envios_recebidos`
- `total_respostas_enviadas`

## 📊 Exemplos de Indicadores

### Taxa de Resposta
```
Taxa de Resposta = COUNT(vw_powerbi_respostas) / COUNT(vw_powerbi_envios)
```

### Distribuição NPS
```
Promotores = COUNT(vw_powerbi_respostas[classificacao_nps] = "Promotor")
Neutros = COUNT(vw_powerbi_respostas[classificacao_nps] = "Neutro")
Detratores = COUNT(vw_powerbi_respostas[classificacao_nps] = "Detrator")
```

### Respostas por Status
```
Respondentes Ativos = COUNT(vw_powerbi_respondentes[status_usuario] = "Ativo")
```

## 🔄 Atualização de Dados

### Modo Import (Recomendado para início)
- Dados são importados uma vez
- Atualização manual ou agendada
- Mais rápido para visualizações

### Modo DirectQuery
- Dados sempre atualizados
- Consultas diretas ao banco
- Mais lento, mas sempre atualizado

## ⚠️ Notas Importantes

1. **Email é obrigatório**: Todas as views filtram registros sem email
2. **Chave única**: Email deve ser único em cada tabela
3. **Performance**: Views são otimizadas, mas use índices para grandes volumes
4. **Segurança**: Não compartilhe credenciais no Power BI Service

## 📚 Recursos Adicionais

- [Documentação Power BI](https://docs.microsoft.com/power-bi/)
- [Supabase PostgreSQL](https://supabase.com/docs/guides/database)
- Views criadas estão no arquivo `database/powerbi_views.sql`

## ✅ Checklist

- [ ] Tabela `respondents` criada
- [ ] Views para Power BI criadas
- [ ] Migração Django executada (opcional)
- [ ] Power BI conectado ao Supabase
- [ ] Views selecionadas no Power BI
- [ ] Relacionamentos criados por EMAIL
- [ ] Primeiros indicadores criados

---

**Pronto para usar!** 🎉
