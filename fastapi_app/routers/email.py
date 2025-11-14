"""
Router para envio de emails via SendGrid
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from services.email import send_email, send_template_email

router = APIRouter()


class EmailRequest(BaseModel):
    """Modelo para requisição de envio de email"""
    to_emails: List[EmailStr]
    subject: str
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    from_email: Optional[str] = None
    from_name: Optional[str] = None
    cc_emails: Optional[List[EmailStr]] = None
    bcc_emails: Optional[List[EmailStr]] = None
    reply_to: Optional[EmailStr] = None
    categories: Optional[List[str]] = None


class TemplateEmailRequest(BaseModel):
    """Modelo para requisição de email com template"""
    to_emails: List[EmailStr]
    template_id: str
    dynamic_template_data: Dict[str, Any]
    from_email: Optional[str] = None
    from_name: Optional[str] = None
    cc_emails: Optional[List[EmailStr]] = None
    bcc_emails: Optional[List[EmailStr]] = None


@router.post("/email/send")
async def send_email_endpoint(
    email_request: EmailRequest,
    background_tasks: BackgroundTasks
):
    """
    Envia um email via SendGrid
    
    Pode ser executado em background ou de forma síncrona
    """
    try:
        result = send_email(
            to_emails=[str(email) for email in email_request.to_emails],
            subject=email_request.subject,
            html_content=email_request.html_content,
            text_content=email_request.text_content,
            from_email=email_request.from_email,
            from_name=email_request.from_name,
            cc_emails=[str(email) for email in email_request.cc_emails] if email_request.cc_emails else None,
            bcc_emails=[str(email) for email in email_request.bcc_emails] if email_request.bcc_emails else None,
            reply_to=str(email_request.reply_to) if email_request.reply_to else None,
            categories=email_request.categories
        )
        
        return {
            "message": "Email enviado com sucesso",
            "status_code": result.get("status_code"),
            "success": result.get("success")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {str(e)}")


@router.post("/email/send-background")
async def send_email_background(
    email_request: EmailRequest,
    background_tasks: BackgroundTasks
):
    """
    Envia um email via SendGrid em background (assíncrono)
    """
    def send_email_task():
        try:
            send_email(
                to_emails=[str(email) for email in email_request.to_emails],
                subject=email_request.subject,
                html_content=email_request.html_content,
                text_content=email_request.text_content,
                from_email=email_request.from_email,
                from_name=email_request.from_name,
                cc_emails=[str(email) for email in email_request.cc_emails] if email_request.cc_emails else None,
                bcc_emails=[str(email) for email in email_request.bcc_emails] if email_request.bcc_emails else None,
                reply_to=str(email_request.reply_to) if email_request.reply_to else None,
                categories=email_request.categories
            )
        except Exception as e:
            # Log do erro (em produção, usar um logger adequado)
            print(f"Erro ao enviar email em background: {str(e)}")
    
    background_tasks.add_task(send_email_task)
    
    return {
        "message": "Email será enviado em background",
        "status": "queued"
    }


@router.post("/email/send-template")
async def send_template_email_endpoint(
    template_request: TemplateEmailRequest,
    background_tasks: BackgroundTasks
):
    """
    Envia um email usando template dinâmico do SendGrid
    """
    try:
        result = send_template_email(
            to_emails=[str(email) for email in template_request.to_emails],
            template_id=template_request.template_id,
            dynamic_template_data=template_request.dynamic_template_data,
            from_email=template_request.from_email,
            from_name=template_request.from_name,
            cc_emails=[str(email) for email in template_request.cc_emails] if template_request.cc_emails else None,
            bcc_emails=[str(email) for email in template_request.bcc_emails] if template_request.bcc_emails else None
        )
        
        return {
            "message": "Email com template enviado com sucesso",
            "status_code": result.get("status_code"),
            "success": result.get("success")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email com template: {str(e)}")

