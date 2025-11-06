# 🔗 Links de Acesso - NPS Surveys

## 🎯 Links Principais

### Django Admin (Gerenciamento)
```
http://localhost:8000/admin/
```
**O que você pode fazer:**
- Gerenciar pesquisas (Surveys)
- Gerenciar perguntas e opções
- Cadastrar respondentes (Respondents)
- Ver convites enviados (Survey Invitations)
- Ver respostas recebidas (Survey Responses)
- Ver resultados NPS calculados
- Criar lista automática de convidados
- Enviar convites por email

---

### Página de Convites de uma Pesquisa
```
http://localhost:8000/survey/{survey_id}/invitations/
```
**Exemplo:** `http://localhost:8000/survey/1/invitations/`

**O que você pode fazer:**
- Ver lista de convites enviados
- Ver tracking de emails (abertura, cliques)
- Criar lista automática de convidados
- Enviar novos convites

---

### Enviar Convites (Formulário)
```
http://localhost:8000/survey/{survey_id}/invite/
```
**Exemplo:** `http://localhost:8000/survey/1/invite/`

**O que você pode fazer:**
- Digitar emails manualmente (um por linha)
- Definir dias de expiração
- Enviar convites por email

---

### Criar Lista Automática de Convidados
```
http://localhost:8000/survey/{survey_id}/criar-lista-convidados/
```
**Exemplo:** `http://localhost:8000/survey/1/criar-lista-convidados/`

**O que você pode fazer:**
- Ver preview da seleção automática
- Confirmar criação de lista (1/6 dos elegíveis)
- Ver estatísticas (total, elegíveis, excluídos)

---

### Dashboard NPS
```
http://localhost:8000/nps/dashboard/
```
**Ou para uma pesquisa específica:**
```
http://localhost:8000/nps/dashboard/{survey_id}/
```
**Exemplo:** `http://localhost:8000/nps/dashboard/1/`

**O que você pode fazer:**
- Ver score NPS
- Ver gráficos de tendência
- Ver resumo (promotores, neutros, detratores)
- Exportar relatórios (Excel, CSV)

---

### Tracking de Emails
```
http://localhost:8000/email-tracking/{survey_id}/
```
**Exemplo:** `http://localhost:8000/email-tracking/1/`

**O que você pode fazer:**
- Ver quem recebeu mas não abriu
- Ver quem abriu mas não clicou
- Ver quem clicou mas não respondeu
- Ver quem respondeu

---

## 📧 Links de Resposta (Para Convidados)

### Responder Pesquisa (Link Único)
```
http://localhost:8000/survey/{survey_id}/respond/{token}/
```
**Exemplo:** `http://localhost:8000/survey/1/respond/550e8400-e29b-41d4-a716-446655440000/`

**Nota:** Este link é único para cada convidado e é gerado automaticamente.

**Como obter o link:**
1. Django Admin → Survey Invitations
2. Selecione um convite
3. Veja o campo "Link do Convite"

---

## 🔧 Links de API

### API REST (Django)
```
http://localhost:8000/api/
```

**Endpoints disponíveis:**
- `GET /api/surveys/` - Lista pesquisas
- `GET /api/surveys/{id}/` - Detalhes de uma pesquisa
- `GET /api/responses/` - Lista respostas
- `GET /api/responses/{id}/` - Detalhes de uma resposta

### API NPS (Dados para gráficos)
```
http://localhost:8000/nps/api/{survey_id}/data/
```
**Exemplo:** `http://localhost:8000/nps/api/1/data/`

### FastAPI (Se estiver rodando)
```
http://localhost:8001/
```
**Documentação Swagger:**
```
http://localhost:8001/docs
```

---

## 📊 Links de Exportação

### Exportar NPS para Excel
```
http://localhost:8000/nps/export/{survey_id}/excel/
```
**Exemplo:** `http://localhost:8000/nps/export/1/excel/`

### Exportar NPS para CSV
```
http://localhost:8000/nps/export/{survey_id}/csv/
```
**Exemplo:** `http://localhost:8000/nps/export/1/csv/`

---

## 🔍 Como Descobrir IDs

### Descobrir ID de uma Pesquisa:
1. Acesse Django Admin
2. Vá em "Surveys"
3. O ID aparece na primeira coluna ou na URL ao editar

### Descobrir Token de um Convite:
1. Django Admin → Survey Invitations
2. Selecione um convite
3. Veja o campo "Unique Token"

---

## 📝 Exemplo Completo de Uso

### 1. Acessar Admin
```
http://localhost:8000/admin/
```
Login com superusuário

### 2. Criar Lista de Convidados
```
http://localhost:8000/survey/1/criar-lista-convidados/
```
(Substitua 1 pelo ID da sua pesquisa)

### 3. Ver Convites Criados
```
http://localhost:8000/survey/1/invitations/
```

### 4. Enviar Convites
```
http://localhost:8000/survey/1/invite/
```

### 5. Ver Dashboard NPS
```
http://localhost:8000/nps/dashboard/1/
```

### 6. Ver Tracking
```
http://localhost:8000/email-tracking/1/
```

---

## ⚠️ Importante

- **Localhost**: Funciona apenas na sua máquina local
- **Produção**: Após deploy, substitua `localhost:8000` pela URL do servidor
- **HTTPS**: Em produção, use `https://` ao invés de `http://`

---

## 🚀 Após Deploy em Produção

Substitua `localhost:8000` pela URL do seu servidor:

**Exemplo Railway:**
```
https://seu-app.railway.app/admin/
https://seu-app.railway.app/survey/1/invitations/
```

**Exemplo Render:**
```
https://seu-app.onrender.com/admin/
https://seu-app.onrender.com/survey/1/invitations/
```

---

**Status**: ✅ Todos os links documentados!

