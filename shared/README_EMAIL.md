# Serviço de Email SendGrid

Este módulo fornece uma integração completa com SendGrid para envio de emails no projeto.

## Configuração Rápida

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variáveis de ambiente no `.env`:**
   ```env
   SENDGRID_API_KEY=sua-chave-api-aqui
   SENDGRID_FROM_EMAIL=noreply@seudominio.com
   SENDGRID_FROM_NAME=NPS Surveys
   ```

3. **Obter API Key do SendGrid:**
   - Acesse https://sendgrid.com/
   - Vá em Settings > API Keys
   - Crie uma nova API Key com permissão "Mail Send"

## Uso Básico

### No FastAPI

```python
from fastapi_app.services.email import send_email

result = send_email(
    to_emails=["cliente@example.com"],
    subject="Bem-vindo!",
    html_content="<h1>Olá!</h1><p>Obrigado por participar.</p>"
)
```

### No Django

```python
from surveys.email_service import send_email_django

result = send_email_django(
    to_emails=["cliente@example.com"],
    subject="Bem-vindo!",
    html_content="<h1>Olá!</h1><p>Obrigado por participar.</p>"
)
```

## Funcionalidades

- ✅ Envio de emails HTML e texto
- ✅ Múltiplos destinatários (TO, CC, BCC)
- ✅ Anexos
- ✅ Templates dinâmicos do SendGrid
- ✅ Envio em background (FastAPI)
- ✅ Categorias para tracking
- ✅ Tratamento de erros

## Documentação Completa

Veja o guia completo em: `docs/SENDGRID_EMAIL_GUIDE.md`

## Exemplos

Veja exemplos práticos em: `examples/email_example.py`

