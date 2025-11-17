# 🧪 Guia de Teste dos Templates

## ✅ Dados de Teste Criados

Dados de teste foram criados com sucesso! Agora você pode testar todos os templates.

## 📋 URLs para Testar

### 1. **Lista de Convites** ✅
**URL**: http://localhost:8000/survey/1/invitations/
- Template: `invitations_list.html`
- Mostra todos os convites da pesquisa
- Estatísticas de envios e respostas
- Ações para reenviar convites

### 2. **Enviar Convites** ✅
**URL**: http://localhost:8000/survey/1/invite/
- Template: `send_invitations.html`
- Formulário para enviar novos convites
- Campo para múltiplos emails
- Configuração de expiração

### 3. **Responder Pesquisa** ✅
**URL**: http://localhost:8000/survey/1/respond/7ff55155-1afa-45ba-bc2a-0848a1963e68/
- Template: `respond_survey.html`
- Formulário para responder pesquisa
- Perguntas NPS, texto e rating
- Validação de campos obrigatórios

**Outros tokens disponíveis:**
- `8fcd3fdf-dec2-4f36-83fb-5d689e7b3a11`
- `3ffcd82e-0490-40cd-868a-e01a7397e647`

### 4. **Página de Agradecimento** ✅
- Template: `survey_thank_you.html`
- Aparece após responder a pesquisa
- Mostra ID e data da resposta

### 5. **Pesquisa Expirada** ⚠️
- Template: `survey_expired.html`
- Para testar: criar convite expirado manualmente

### 6. **Já Respondido** ⚠️
- Template: `survey_already_answered.html`
- Para testar: tentar responder novamente com mesmo token

## 🚀 Como Iniciar o Servidor

### Opção 1: Script Automático
```powershell
.\iniciar_corrigido.ps1
```

### Opção 2: Manual
```powershell
cd django_app
..\venv\Scripts\python.exe manage.py runserver
```

## 🧪 Testes Recomendados

### Teste 1: Lista de Convites
1. Acesse: http://localhost:8000/survey/1/invitations/
2. Verifique:
   - ✅ Tabela com convites
   - ✅ Status de cada convite
   - ✅ Botão "Enviar Novos Convites"
   - ✅ Estatísticas no topo

### Teste 2: Enviar Convites
1. Acesse: http://localhost:8000/survey/1/invite/
2. Preencha:
   - Emails (um por linha)
   - Dias de expiração
3. Clique em "Enviar Convites"
4. Verifique redirecionamento para lista

### Teste 3: Responder Pesquisa
1. Acesse uma URL de resposta (exemplo acima)
2. Preencha todas as perguntas
3. Clique em "Enviar Resposta"
4. Verifique página de agradecimento

### Teste 4: Template Expirado
1. No Django Admin, edite um convite
2. Altere `expires_at` para data passada
3. Tente acessar a URL do convite
4. Deve mostrar `survey_expired.html`

### Teste 5: Template Já Respondido
1. Responda uma pesquisa
2. Tente acessar a mesma URL novamente
3. Deve mostrar `survey_already_answered.html`

## 📊 Dados de Teste Criados

- **Pesquisa ID**: 1
- **Título**: "Pesquisa de Satisfação NPS - Teste"
- **Perguntas**: 3 (NPS, Texto, Rating)
- **Convites**: 3 criados
- **Respondentes**: 3 cadastrados

## 🔍 Verificar no Admin

Acesse: http://localhost:8000/admin/

Você pode ver:
- Pesquisas criadas
- Convites enviados
- Respostas recebidas
- Respondentes cadastrados

## ⚠️ Problemas Comuns

### Servidor não está rodando
```powershell
cd django_app
..\venv\Scripts\python.exe manage.py runserver
```

### Erro 404 - URL não encontrada
- Verifique se o servidor está rodando
- Confirme que as URLs estão integradas (ponto 3.1)

### Template não encontrado
- Verifique se os templates estão em `django_app/templates/surveys/`
- Verifique se `settings.py` tem `APP_DIRS = True`

## ✅ Checklist de Testes

- [ ] Lista de convites carrega corretamente
- [ ] Formulário de envio funciona
- [ ] Convites podem ser enviados
- [ ] Formulário de resposta funciona
- [ ] Respostas são salvas
- [ ] Página de agradecimento aparece
- [ ] Template expirado funciona
- [ ] Template já respondido funciona
- [ ] Design responsivo funciona
- [ ] Mensagens de erro aparecem

---

**Pronto para testar!** 🎉
