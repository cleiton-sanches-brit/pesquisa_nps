# Arquitetura de Envio de Emails com SendGrid

## 📧 Como Funciona o SendGrid

O **SendGrid é um serviço de envio de emails na nuvem**. Ele funciona independentemente de onde seu formulário ou aplicação está hospedada.

### ✅ O que você NÃO precisa:

- ❌ Hospedar o formulário em cloud especificamente para usar SendGrid
- ❌ Servidor de email próprio
- ❌ Configuração de SMTP complexa

### ✅ O que você precisa:

- ✅ API Key do SendGrid (gratuita até 100 emails/dia)
- ✅ Código que chama a API do SendGrid (pode estar em qualquer lugar)
- ✅ Aplicação acessível (se quiser receber respostas via web)

## 🏗️ Opções de Arquitetura

### Opção 1: Formulário Local + API Cloud (Recomendado)

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Formulário     │  POST   │  FastAPI     │  API    │  SendGrid   │
│  (Qualquer      │ ───────>│  (Cloud)     │ ───────>│  (Cloud)    │
│   lugar)        │         │  Porta 8001  │         │             │
└─────────────────┘         └──────────────┘         └─────────────┘
                                      │
                                      │ Salva resposta
                                      ▼
                              ┌──────────────┐
                              │  Database    │
                              │  (Cloud)     │
                              └──────────────┘
```

**Vantagens:**
- Formulário pode estar em qualquer lugar (local, Power Automate, SharePoint, etc)
- API hospedada em cloud (Azure, AWS, Heroku, etc)
- SendGrid sempre na nuvem (não precisa hospedar)

**Exemplo:**
- Formulário: Power Automate, SharePoint, ou HTML simples
- API: Azure App Service, AWS Lambda, Heroku
- SendGrid: Serviço gerenciado (você só usa a API)

### Opção 2: Tudo Local (Desenvolvimento)

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Formulário     │  POST   │  FastAPI     │  API    │  SendGrid   │
│  (localhost)    │ ───────>│  (localhost) │ ───────>│  (Cloud)    │
│  Porta 3000    │         │  Porta 8001  │         │             │
└─────────────────┘         └──────────────┘         └─────────────┘
```

**Vantagens:**
- Desenvolvimento rápido
- Testes locais
- SendGrid funciona normalmente (só precisa da API key)

**Limitações:**
- Não acessível externamente
- Apenas para desenvolvimento/testes

### Opção 3: Formulário Integrado (SPA)

```
┌─────────────────────────────────────────────────┐
│  Aplicação Web Completa (React/Vue/Angular)    │
│  ┌──────────┐         ┌──────────┐             │
│  │Formulário│  POST   │  FastAPI │             │
│  │          │ ───────>│          │             │
│  └──────────┘         └──────────┘             │
│                           │                     │
│                           │ Envia email         │
│                           ▼                     │
│                    ┌─────────────┐              │
│                    │  SendGrid   │              │
│                    │  (Cloud)    │              │
│                    └─────────────┘              │
└─────────────────────────────────────────────────┘
```

**Vantagens:**
- Tudo em um lugar
- Experiência do usuário integrada
- Fácil de manter

## 🎯 Cenários Práticos

### Cenário 1: Power Automate + Azure

**Onde cada coisa fica:**
- **Formulário**: Power Automate (Microsoft Flow)
- **API FastAPI**: Azure App Service
- **SendGrid**: Serviço gerenciado (você só usa)

**Fluxo:**
1. Usuário preenche formulário no Power Automate
2. Power Automate chama sua API no Azure: `POST https://sua-api.azurewebsites.net/api/v1/responses`
3. API salva no banco e envia email via SendGrid
4. Email chega no destinatário

### Cenário 2: SharePoint + Azure

**Onde cada coisa fica:**
- **Formulário**: SharePoint List ou Power Apps
- **API FastAPI**: Azure App Service
- **SendGrid**: Serviço gerenciado

**Fluxo:**
1. Usuário preenche formulário no SharePoint
2. SharePoint chama sua API via HTTP Request
3. API processa e envia email via SendGrid

### Cenário 3: HTML Simples + Heroku

**Onde cada coisa fica:**
- **Formulário**: HTML estático (pode estar em qualquer lugar)
- **API FastAPI**: Heroku
- **SendGrid**: Serviço gerenciado

**Fluxo:**
1. Usuário acessa formulário HTML
2. JavaScript envia dados para API no Heroku
3. API envia email via SendGrid

## 🔑 Pontos Importantes

### 1. SendGrid é sempre na nuvem
- Você não hospeda o SendGrid
- Você apenas usa a API deles
- Funciona de qualquer lugar que tenha internet

### 2. O que precisa estar acessível?
- **API FastAPI**: Precisa estar acessível se o formulário for externo
- **Formulário**: Depende de onde você quer que os usuários acessem
- **SendGrid**: Já está na nuvem (você não hospeda)

### 3. Para desenvolvimento local
- Tudo pode rodar localmente
- SendGrid funciona normalmente (só precisa da API key)
- Útil para testes

## 📋 Checklist de Deploy

### Para Produção:

- [ ] API FastAPI hospedada em cloud (Azure, AWS, Heroku, etc)
- [ ] Variável `SENDGRID_API_KEY` configurada no ambiente
- [ ] Variável `SENDGRID_FROM_EMAIL` configurada (email verificado no SendGrid)
- [ ] Formulário acessível aos usuários finais
- [ ] CORS configurado na API (se formulário estiver em domínio diferente)
- [ ] HTTPS configurado (recomendado)

### Para Desenvolvimento:

- [ ] API rodando localmente (`uvicorn main:app --reload`)
- [ ] Variáveis de ambiente no arquivo `.env`
- [ ] SendGrid API Key configurada
- [ ] Formulário de teste funcionando

## 💡 Recomendações

### Para começar rápido:
1. **Desenvolvimento**: Tudo local (localhost)
2. **Testes**: Use SendGrid em modo sandbox (gratuito)
3. **Produção**: Hospede a API em Azure/AWS/Heroku

### Para produção:
1. **API**: Azure App Service ou AWS Elastic Beanstalk
2. **Formulário**: Onde for mais conveniente (Power Automate, SharePoint, HTML)
3. **SendGrid**: Já está pronto (só configurar API key)

## 🚀 Exemplo Prático: Deploy no Azure

```bash
# 1. Criar App Service no Azure
az webapp create --name minha-api-nps --resource-group meu-rg

# 2. Configurar variáveis de ambiente
az webapp config appsettings set \
  --name minha-api-nps \
  --resource-group meu-rg \
  --settings SENDGRID_API_KEY="sua-chave-aqui"

# 3. Fazer deploy
git push azure main
```

Depois disso, sua API estará acessível em:
```
https://minha-api-nps.azurewebsites.net/api/v1/email/send
```

E o SendGrid funcionará normalmente, mesmo que o formulário esteja em outro lugar!

## ❓ FAQ

**P: Preciso hospedar o formulário em cloud para usar SendGrid?**
R: Não! O SendGrid funciona de qualquer lugar. O que importa é que sua API (que chama o SendGrid) esteja acessível.

**P: Posso usar SendGrid com formulário local?**
R: Sim! Para desenvolvimento, tudo pode rodar localmente. O SendGrid funciona normalmente.

**P: O SendGrid precisa estar no mesmo servidor que minha API?**
R: Não! O SendGrid é um serviço separado na nuvem. Você só precisa da API key.

**P: Posso usar SendGrid com Power Automate?**
R: Sim! O Power Automate pode chamar sua API, que por sua vez chama o SendGrid.

## 📚 Referências

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Azure App Service](https://azure.microsoft.com/services/app-service/)
- [Heroku Deploy](https://devcenter.heroku.com/articles/getting-started-with-python)


