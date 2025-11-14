# Guia de Envio de Emails com SendGrid

Este guia explica como usar o serviço de envio de emails via SendGrid no projeto de pesquisas NPS.

## Configuração Inicial

### 1. Obter API Key do SendGrid

1. Acesse [SendGrid](https://sendgrid.com/) e crie uma conta (se ainda não tiver)
2. Vá em **Settings** > **API Keys**
3. Clique em **Create API Key**
4. Dê um nome à chave (ex: "NPS Surveys Production")
5. Selecione as permissões necessárias (pelo menos **Mail Send** > **Full Access**)
6. Copie a API Key gerada (ela só será mostrada uma vez!)

### 2. Configurar Variáveis de Ambiente

Adicione as seguintes variáveis ao seu arquivo `.env`:

```env
# SendGrid Email Settings
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@seudominio.com
SENDGRID_FROM_NAME=NPS Surveys
```

**Importante:**
- `SENDGRID_API_KEY`: Sua chave API do SendGrid
- `SENDGRID_FROM_EMAIL`: Email verificado no SendGrid (deve estar verificado no SendGrid)
- `SENDGRID_FROM_NAME`: Nome que aparecerá como remetente

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

A biblioteca `sendgrid==6.11.0` já está incluída no `requirements.txt`.

## Uso no FastAPI

### Exemplo 1: Envio Simples de Email

```python
from fastapi_app.services.email import send_email

# Enviar email simples
result = send_email(
    to_emails=["cliente@example.com"],
    subject="Bem-vindo à Pesquisa NPS",
    html_content="""
    <h1>Olá!</h1>
    <p>Obrigado por participar da nossa pesquisa NPS.</p>
    <p>Seu feedback é muito importante para nós.</p>
    """,
    text_content="Olá! Obrigado por participar da nossa pesquisa NPS."
)

print(f"Email enviado: {result['success']}")
```

### Exemplo 2: Usando o Endpoint da API

```python
import requests

# Enviar email via endpoint
response = requests.post(
    "http://localhost:8001/api/v1/email/send",
    json={
        "to_emails": ["cliente@example.com"],
        "subject": "Bem-vindo à Pesquisa NPS",
        "html_content": "<h1>Olá!</h1><p>Obrigado por participar.</p>",
        "text_content": "Olá! Obrigado por participar."
    }
)

print(response.json())
```

### Exemplo 3: Envio em Background

```python
# No seu router FastAPI
from fastapi import BackgroundTasks
from fastapi_app.services.email import send_email

@router.post("/survey/{survey_id}/notify")
async def notify_survey_completion(
    survey_id: int,
    background_tasks: BackgroundTasks
):
    # Enviar email em background (não bloqueia a resposta)
    def send_notification():
        send_email(
            to_emails=["admin@example.com"],
            subject=f"Pesquisa {survey_id} completada",
            html_content=f"<p>A pesquisa {survey_id} foi completada.</p>"
        )
    
    background_tasks.add_task(send_notification)
    return {"message": "Notificação será enviada"}
```

### Exemplo 4: Email com Anexo

```python
from fastapi_app.services.email import send_email

# Ler arquivo para anexar
with open("relatorio.pdf", "rb") as f:
    pdf_content = f.read()

result = send_email(
    to_emails=["admin@example.com"],
    subject="Relatório de Pesquisas",
    html_content="<p>Segue em anexo o relatório.</p>",
    attachments=[{
        "filename": "relatorio.pdf",
        "content": pdf_content,
        "type": "application/pdf"
    }]
)
```

### Exemplo 5: Usando Templates Dinâmicos do SendGrid

Primeiro, crie um template no SendGrid:
1. Acesse **Email API** > **Dynamic Templates**
2. Crie um novo template
3. Use variáveis como `{{nome}}`, `{{link}}`, etc.
4. Copie o **Template ID**

```python
from fastapi_app.services.email import send_template_email

result = send_template_email(
    to_emails=["cliente@example.com"],
    template_id="d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    dynamic_template_data={
        "nome": "João Silva",
        "link": "https://example.com/pesquisa/123",
        "empresa": "Minha Empresa"
    }
)
```

## Uso no Django

### Exemplo 1: Envio Simples

```python
from surveys.email_service import send_email_django

# Em uma view ou signal
def enviar_email_confirmacao(usuario_email):
    result = send_email_django(
        to_emails=[usuario_email],
        subject="Confirmação de Cadastro",
        html_content="""
        <h1>Bem-vindo!</h1>
        <p>Seu cadastro foi confirmado com sucesso.</p>
        """
    )
    return result
```

### Exemplo 2: Em um Signal do Django

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from surveys.models import SurveyResponse
from surveys.email_service import send_email_django

@receiver(post_save, sender=SurveyResponse)
def enviar_email_resposta(sender, instance, created, **kwargs):
    if created:
        send_email_django(
            to_emails=[instance.respondent_email],
            subject="Obrigado pela sua resposta!",
            html_content=f"""
            <h1>Obrigado!</h1>
            <p>Sua resposta foi registrada com sucesso.</p>
            <p>ID da Resposta: {instance.id}</p>
            """
        )
```

### Exemplo 3: Em uma View

```python
from django.http import JsonResponse
from surveys.email_service import send_email_django

def enviar_relatorio(request):
    try:
        result = send_email_django(
            to_emails=["admin@example.com"],
            subject="Relatório Semanal",
            html_content="<p>Segue o relatório semanal.</p>",
            attachments=[{
                "filename": "relatorio.xlsx",
                "content": excel_file_bytes,
                "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }]
        )
        return JsonResponse({"success": True, "result": result})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
```

## Endpoints da API (FastAPI)

### POST `/api/v1/email/send`

Envia um email de forma síncrona.

**Request Body:**
```json
{
  "to_emails": ["cliente@example.com"],
  "subject": "Assunto do Email",
  "html_content": "<h1>Conteúdo HTML</h1>",
  "text_content": "Conteúdo texto (opcional)",
  "from_email": "noreply@example.com",
  "from_name": "NPS Surveys",
  "cc_emails": ["copia@example.com"],
  "bcc_emails": ["oculto@example.com"],
  "reply_to": "suporte@example.com",
  "categories": ["nps", "notification"]
}
```

### POST `/api/v1/email/send-background`

Envia um email de forma assíncrona (em background).

**Request Body:** Mesmo formato do endpoint anterior.

### POST `/api/v1/email/send-template`

Envia um email usando template dinâmico do SendGrid.

**Request Body:**
```json
{
  "to_emails": ["cliente@example.com"],
  "template_id": "d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "dynamic_template_data": {
    "nome": "João Silva",
    "link": "https://example.com/pesquisa/123"
  },
  "from_email": "noreply@example.com",
  "from_name": "NPS Surveys"
}
```

## Tratamento de Erros

O serviço lança exceções em caso de erro. Sempre use try/except:

```python
from fastapi_app.services.email import send_email

try:
    result = send_email(
        to_emails=["cliente@example.com"],
        subject="Teste",
        html_content="<p>Teste</p>"
    )
    if result['success']:
        print("Email enviado com sucesso!")
    else:
        print(f"Erro: Status {result['status_code']}")
except ValueError as e:
    print(f"Erro de configuração: {e}")
except Exception as e:
    print(f"Erro ao enviar email: {e}")
```

## Boas Práticas

1. **Sempre valide emails**: Use `email-validator` ou validação do Pydantic
2. **Use templates**: Para emails recorrentes, use templates do SendGrid
3. **Envio em background**: Para emails não críticos, use background tasks
4. **Tratamento de erros**: Sempre trate exceções e logue erros
5. **Rate limiting**: SendGrid tem limites de envio (verifique seu plano)
6. **Verificar domínio**: Configure SPF, DKIM e DMARC no SendGrid
7. **Testes**: Use o modo de teste do SendGrid durante desenvolvimento

## Limites do SendGrid

- **Free Tier**: 100 emails/dia
- **Essentials**: 40.000 emails/mês
- **Pro**: 100.000+ emails/mês

Verifique seu plano em: https://sendgrid.com/pricing/

## Documentação Adicional

- [SendGrid Python SDK](https://github.com/sendgrid/sendgrid-python)
- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference)
- [Dynamic Templates](https://docs.sendgrid.com/ui/sending-email/how-to-send-an-email-with-dynamic-templates)

