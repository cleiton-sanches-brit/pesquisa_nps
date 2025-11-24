# 🚀 Próximos Passos - Deploy e Finalização

Este documento descreve os passos necessários para finalizar o projeto e fazer o deploy no Azure.

## ✅ Status Atual

- ✅ Projeto limpo e organizado
- ✅ Estrutura Django configurada
- ✅ SendGrid configurado para envio de emails
- ✅ Configuração para Azure SQL Database
- ✅ Templates de email criados
- ✅ Formulário de pesquisa funcional
- ✅ Dashboard NPS implementado
- ✅ Exportação de dados (CSV/Excel)
- ⏳ Pendente: Commit no GitHub
- ⏳ Pendente: Configuração do Azure App Service
- ⏳ Pendente: Configuração de variáveis de ambiente no Azure
- ⏳ Pendente: Liberação de IPs do banco de dados
- ⏳ Pendente: Testes finais em produção

---

## 📋 Checklist de Próximos Passos

### 1. Commit e Push para GitHub

**Objetivo:** Salvar o estado atual do projeto no repositório

```bash
cd pesquisas_nps
git add .
git commit -m "Limpeza do projeto - remoção de arquivos desnecessários"
git push origin main
```

**Verificação:**
- [ ] Todos os arquivos necessários foram commitados
- [ ] Arquivo `.env` NÃO foi commitado (está no .gitignore)
- [ ] Código está no repositório remoto

---

### 2. Configuração do Azure App Service

**Objetivo:** Criar e configurar o serviço de hospedagem no Azure

#### 2.1. Criar App Service no Azure Portal

1. Acesse o [Azure Portal](https://portal.azure.com)
2. Vá em **App Services** → **Criar**
3. Configure:
   - **Nome:** `pesquisas-nps` (ou outro nome disponível)
   - **Sistema Operacional:** Linux
   - **Runtime Stack:** Python 3.12
   - **Plano:** Escolha conforme necessidade (B1 Basic recomendado para início)
   - **Região:** Mesma região do banco de dados

#### 2.2. Configurar Deployment

**Opção 1: Deploy via GitHub (Recomendado)**
1. No App Service, vá em **Deployment Center**
2. Selecione **GitHub** como fonte
3. Autorize e selecione o repositório: `cleiton-sanches-brit/pesquisa_nps`
4. Selecione a branch: `main`
5. Configure o caminho: `django_app` (pasta onde está o `manage.py`)

**Opção 2: Deploy via Azure CLI**
```bash
az webapp up --name pesquisas-nps --resource-group seu-resource-group --runtime "PYTHON:3.12"
```

**Verificação:**
- [ ] App Service criado
- [ ] Deployment configurado
- [ ] Código está sendo deployado automaticamente

---

### 3. Configurar Variáveis de Ambiente no Azure

**Objetivo:** Configurar todas as variáveis necessárias para produção

No Azure Portal, vá em **App Service** → **Configuration** → **Application settings**

Adicione as seguintes variáveis:

```env
# Django Settings
SECRET_KEY=<gerar-chave-secreta-forte>
DEBUG=False
ALLOWED_HOSTS=pesquisas-nps.azurewebsites.net,seu-dominio.com
CSRF_TRUSTED_ORIGINS=https://pesquisas-nps.azurewebsites.net,https://seu-dominio.com

# Database Settings - Azure SQL
DB_HOST=seu-servidor-azure.database.windows.net
DB_PORT=1433
DB_NAME=dbNPS
DB_USER=user-nps
DB_PASSWORD=<senha-do-banco>

# SendGrid Email
SENDGRID_API_KEY=<sua-api-key-sendgrid>
SENDGRID_FROM_EMAIL=no-reply@br-itsoftware.com.br
SENDGRID_FROM_NAME=BR-IT Software
```

**Gerar SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**Verificação:**
- [ ] Todas as variáveis configuradas
- [ ] SECRET_KEY gerada e configurada
- [ ] DEBUG=False em produção
- [ ] SendGrid API Key configurada
- [ ] Credenciais do banco configuradas

---

### 4. Configurar Azure SQL Database

**Objetivo:** Permitir conexão do App Service ao banco de dados

#### 4.1. Liberar IPs do App Service

1. No Azure Portal, vá em **SQL Server** → **Firewalls e redes virtuais**
2. Adicione regra para permitir serviços do Azure:
   - Marque **Permitir que os serviços e recursos do Azure acessem este servidor**
3. Adicione IPs do App Service:
   - Vá em **App Service** → **Propriedades** → copie o **Outbound IP addresses**
   - Adicione cada IP como regra de firewall no SQL Server

**Alternativa: Configurar Firewall via Azure CLI**
```bash
# Permitir serviços do Azure
az sql server firewall-rule create \
  --resource-group seu-resource-group \
  --server seu-servidor-sql \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Adicionar IP específico do App Service
az sql server firewall-rule create \
  --resource-group seu-resource-group \
  --server seu-servidor-sql \
  --name AllowAppService \
  --start-ip-address <IP-DO-APP-SERVICE> \
  --end-ip-address <IP-DO-APP-SERVICE>
```

#### 4.2. Executar Migrações

Após o deploy, execute as migrações do banco de dados:

**Opção 1: Via SSH no App Service**
1. No App Service, vá em **SSH**
2. Execute:
```bash
cd django_app
python manage.py migrate
python manage.py createsuperuser
```

**Opção 2: Via Azure CLI**
```bash
az webapp ssh --name pesquisas-nps --resource-group seu-resource-group
cd django_app
python manage.py migrate
python manage.py createsuperuser
```

**Verificação:**
- [ ] Firewall do SQL Server configurado
- [ ] IPs do App Service liberados
- [ ] Migrações executadas
- [ ] Superusuário criado

---

### 5. Configurar Domínio Personalizado (Opcional)

**Objetivo:** Usar domínio próprio ao invés de `.azurewebsites.net`

1. No App Service, vá em **Custom domains**
2. Adicione seu domínio
3. Configure os registros DNS conforme instruções do Azure
4. Atualize `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` com o novo domínio

**Verificação:**
- [ ] Domínio configurado
- [ ] Certificado SSL configurado (HTTPS)
- [ ] Variáveis de ambiente atualizadas

---

### 6. Testes em Produção

**Objetivo:** Validar que tudo está funcionando corretamente

#### 6.1. Testes Básicos

1. **Acessar Admin:**
   - URL: `https://pesquisas-nps.azurewebsites.net/admin/`
   - [ ] Login funciona
   - [ ] Interface carrega corretamente

2. **Criar Pesquisa:**
   - [ ] Criar nova pesquisa no admin
   - [ ] Configurar perguntas
   - [ ] Salvar com sucesso

3. **Enviar Convite:**
   - [ ] Criar lista de convidados
   - [ ] Enviar convites por email
   - [ ] Verificar recebimento do email

4. **Responder Pesquisa:**
   - [ ] Clicar no link do email
   - [ ] Formulário carrega corretamente
   - [ ] Preencher e enviar resposta
   - [ ] Mensagem de agradecimento aparece

5. **Dashboard NPS:**
   - URL: `https://pesquisas-nps.azurewebsites.net/nps/dashboard/`
   - [ ] Dashboard carrega
   - [ ] Dados são exibidos corretamente
   - [ ] Gráficos funcionam

6. **Exportação:**
   - [ ] Exportar CSV funciona
   - [ ] Exportar Excel funciona
   - [ ] Dados exportados estão corretos

#### 6.2. Testes de Email

- [ ] Emails são enviados via SendGrid
- [ ] Links nos emails funcionam
- [ ] Template de email está correto
- [ ] Tracking de abertura funciona (se implementado)

#### 6.3. Testes de Performance

- [ ] Páginas carregam rapidamente
- [ ] Formulário responde rapidamente
- [ ] Dashboard carrega sem erros

**Verificação:**
- [ ] Todos os testes básicos passaram
- [ ] Emails sendo enviados corretamente
- [ ] Formulário funcionando
- [ ] Dashboard exibindo dados

---

### 7. Monitoramento e Logs

**Objetivo:** Configurar monitoramento da aplicação

1. **Application Insights (Recomendado):**
   - No App Service, vá em **Application Insights**
   - Crie ou conecte um recurso de Application Insights
   - Configure alertas para erros

2. **Logs:**
   - Configure **Log stream** para ver logs em tempo real
   - Configure **App Service logs** para salvar logs

**Verificação:**
- [ ] Application Insights configurado
- [ ] Logs sendo coletados
- [ ] Alertas configurados

---

### 8. Backup e Segurança

**Objetivo:** Garantir segurança e backup dos dados

1. **Backup do Banco de Dados:**
   - Configure backup automático no Azure SQL Database
   - Defina retenção conforme necessidade

2. **Segurança:**
   - Verifique que `DEBUG=False` em produção
   - Verifique que `SECRET_KEY` está seguro
   - Revise permissões do banco de dados
   - Configure HTTPS obrigatório

**Verificação:**
- [ ] Backup configurado
- [ ] Segurança revisada
- [ ] HTTPS configurado

---

## 📝 Resumo das URLs Importantes

Após o deploy, você terá acesso a:

- **Admin Django:** `https://pesquisas-nps.azurewebsites.net/admin/`
- **Dashboard NPS:** `https://pesquisas-nps.azurewebsites.net/nps/dashboard/`
- **Formulário de Resposta:** `https://pesquisas-nps.azurewebsites.net/survey/<id>/respond/<token>/`
- **Exportação:** `https://pesquisas-nps.azurewebsites.net/nps/export/`

---

## 🔧 Comandos Úteis

### Ver logs do App Service
```bash
az webapp log tail --name pesquisas-nps --resource-group seu-resource-group
```

### Reiniciar App Service
```bash
az webapp restart --name pesquisas-nps --resource-group seu-resource-group
```

### Executar comando no App Service
```bash
az webapp ssh --name pesquisas-nps --resource-group seu-resource-group
```

### Ver variáveis de ambiente
```bash
az webapp config appsettings list --name pesquisas-nps --resource-group seu-resource-group
```

---

## ⚠️ Problemas Comuns e Soluções

### Erro: "Could not connect to database"
- **Solução:** Verificar firewall do SQL Server e IPs liberados

### Erro: "Email not sent"
- **Solução:** Verificar `SENDGRID_API_KEY` e configurações de email

### Erro: "Static files not found"
- **Solução:** Executar `python manage.py collectstatic` no App Service

### Erro: "CSRF verification failed"
- **Solução:** Verificar `CSRF_TRUSTED_ORIGINS` com o domínio correto

### Erro: "Module not found"
- **Solução:** Verificar `requirements.txt` e reinstalar dependências

---

## 📞 Suporte

Em caso de dúvidas ou problemas:

1. Verificar logs do App Service
2. Verificar Application Insights
3. Revisar configurações de variáveis de ambiente
4. Verificar documentação do Azure

---

## ✅ Checklist Final

Antes de considerar o projeto finalizado:

- [ ] Código commitado no GitHub
- [ ] App Service criado e configurado
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados acessível
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Testes em produção realizados
- [ ] Emails sendo enviados
- [ ] Formulário funcionando
- [ ] Dashboard exibindo dados
- [ ] Monitoramento configurado
- [ ] Backup configurado
- [ ] Documentação atualizada

---

**Última atualização:** Novembro 2025

