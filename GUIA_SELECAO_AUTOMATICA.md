# 🎲 Guia: Seleção Automática de Convidados

## 📋 Funcionalidade

Sistema automático para selecionar convidados para pesquisas NPS seguindo critérios específicos.

## 🎯 Critérios de Seleção

### 1. Seleção Aleatória
- Seleciona **1/6 (16.67%)** dos emails da tabela `surveys_respondent`
- Seleção é **aleatória** (randomizada)

### 2. Validação de Período
- Verifica a tabela `surveys_invitation`
- Exclui emails que receberam convite nos **últimos 180 dias**
- Validação considera `sent_at` (data de envio)
- **Independente** se o convidado respondeu ou não

## 🚀 Como Usar

### Opção 1: Via Interface Web (Recomendado)

1. Acesse Django Admin: http://localhost:8000/admin
2. Vá em **"Surveys"** > Selecione uma pesquisa
3. Clique em **"🎲 Criar Lista Automática"** (botão verde)
4. Visualize o preview da seleção
5. Clique em **"Confirmar e Criar Lista de Convidados"**
6. Os convites serão criados (mas não enviados)
7. Use **"Enviar Convites"** para enviar os emails

### Opção 2: Via Página de Convites

1. Acesse: http://localhost:8000/survey/{survey_id}/invitations/
2. Clique no botão **"🎲 Criar Lista Automática"**
3. Siga o mesmo processo acima

### Opção 3: Via Comando Django (Terminal)

```bash
cd django_app
python manage.py criar_lista_convidados <survey_id>
```

Exemplo:
```bash
python manage.py criar_lista_convidados 1
```

Com percentual customizado:
```bash
python manage.py criar_lista_convidados 1 --percentual 0.2
```

## 📊 O que o Sistema Faz

### Passo 1: Buscar Respondentes
- Busca todos os respondentes **ativos** na tabela `surveys_respondent`
- Conta o total disponível

### Passo 2: Filtrar Elegíveis
- Busca convites enviados nos últimos **180 dias** (qualquer pesquisa)
- Cria lista de emails **excluídos**
- Filtra respondentes que **não estão** na lista de excluídos

### Passo 3: Seleção Aleatória
- Calcula **1/6** do total de elegíveis
- Seleciona aleatoriamente essa quantidade
- Garante pelo menos 1 email se houver elegíveis

### Passo 4: Criar Convites
- Cria `SurveyInvitation` para cada email selecionado
- Expiração: **30 dias** a partir da criação
- **Não envia emails** automaticamente

## 📈 Estatísticas Exibidas

Ao criar a lista, você verá:

- **Total de Respondentes**: Todos os respondentes ativos
- **Elegíveis**: Emails que podem receber convite (não receberam nos últimos 180 dias)
- **Excluídos**: Emails que receberam convite recentemente
- **Serão Selecionados**: Quantidade que será selecionada (1/6)

## ⚙️ Configurações

### Percentual de Seleção

Por padrão, seleciona **1/6 (16.67%)**. Para alterar:

**Via código:**
```python
from surveys.utils_selecao import criar_convites_automaticos
resultado = criar_convites_automaticos(survey_id, percentual=0.2)  # 20%
```

**Via comando:**
```bash
python manage.py criar_lista_convidados 1 --percentual 0.2
```

### Período de Exclusão

Por padrão, exclui emails que receberam convite nos **últimos 180 dias**. 

Para alterar, edite `utils_selecao.py`:
```python
data_limite = timezone.now() - timedelta(days=180)  # Altere aqui
```

## 🔄 Fluxo Completo

### 1. Criar Lista de Convidados
- Botão "🎲 Criar Lista Automática"
- Sistema seleciona aleatoriamente 1/6 dos elegíveis
- Cria convites (não envia)

### 2. Enviar Convites
- Botão "Enviar Convites"
- Envia emails para os convites criados
- Marca `sent_at` com data/hora do envio

### 3. Próxima Seleção (1 mês depois)
- Sistema verifica `sent_at`
- Se passaram menos de 180 dias → **excluído**
- Se passaram 180+ dias → **elegível novamente**

## 📝 Exemplo Prático

### Cenário:
- Total de respondentes: **600**
- Receberam convite nos últimos 180 dias: **100**
- Elegíveis: **500**
- 1/6 de 500: **~83 emails**

### Resultado:
- Sistema seleciona aleatoriamente **83 emails**
- Cria **83 convites**
- Você envia os emails
- Próxima seleção (1 mês): esses 83 estarão excluídos

## ✅ Validações

### O que o sistema verifica:
- ✅ Respondente está ativo (`active=True`)
- ✅ Email não recebeu convite nos últimos 180 dias
- ✅ Email não tem convite existente para esta pesquisa

### O que o sistema NÃO verifica:
- ❌ Se o convidado respondeu ou não (não importa)
- ❌ Qual pesquisa recebeu (qualquer pesquisa conta)
- ❌ Se o convite foi usado (`is_used`)

## 🎯 Casos de Uso

### Envio Mensal Automatizado

1. **Mês 1**: Seleciona 1/6 dos 600 = 100 emails
2. **Mês 2**: Seleciona 1/6 dos 500 elegíveis = 83 emails
3. **Mês 3**: Seleciona 1/6 dos 417 elegíveis = 69 emails
4. E assim por diante...

Após 6 meses, os emails do mês 1 voltam a ser elegíveis!

## 📁 Arquivos Criados

- `surveys/utils_selecao.py` - Funções de seleção
- `surveys/views_selecao.py` - Views para interface web
- `surveys/management/commands/criar_lista_convidados.py` - Comando terminal
- `templates/surveys/criar_lista_convidados.html` - Interface de criação

## 🆘 Resolução de Problemas

### Nenhum email elegível
- **Causa**: Todos receberam convite nos últimos 180 dias
- **Solução**: Aguarde mais tempo ou reduza o período de exclusão

### Poucos emails selecionados
- **Causa**: Poucos respondentes elegíveis
- **Solução**: Verifique se há respondentes ativos e se não receberam convite recente

### Email não aparece na lista
- **Causa**: Recebeu convite recentemente ou está inativo
- **Solução**: Verifique `sent_at` na tabela `surveys_invitation`

---

**Status**: ✅ Sistema de seleção automática implementado e pronto para uso!

