"""
Serviço de email para FastAPI usando SendGrid
"""
import sys
from pathlib import Path

# Adicionar o diretório shared ao path
project_root = Path(__file__).resolve().parent.parent.parent
shared_path = project_root / "shared"
sys.path.insert(0, str(shared_path))

from shared.email_service import EmailService, get_email_service
from typing import List, Optional, Dict, Any


def send_email(
    to_emails: List[str],
    subject: str,
    html_content: Optional[str] = None,
    text_content: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    cc_emails: Optional[List[str]] = None,
    bcc_emails: Optional[List[str]] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
    reply_to: Optional[str] = None,
    categories: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Função helper para enviar email via SendGrid no FastAPI
    
    Args:
        to_emails: Lista de emails destinatários
        subject: Assunto do email
        html_content: Conteúdo HTML do email
        text_content: Conteúdo texto do email
        from_email: Email remetente
        from_name: Nome do remetente
        cc_emails: Lista de emails em cópia
        bcc_emails: Lista de emails em cópia oculta
        attachments: Lista de anexos
        reply_to: Email para resposta
        categories: Categorias para tracking
        
    Returns:
        Dict com resultado do envio
    """
    email_service = get_email_service()
    return email_service.send_email(
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
        from_email=from_email,
        from_name=from_name,
        cc_emails=cc_emails,
        bcc_emails=bcc_emails,
        attachments=attachments,
        reply_to=reply_to,
        categories=categories
    )


def send_template_email(
    to_emails: List[str],
    template_id: str,
    dynamic_template_data: Dict[str, Any],
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
    cc_emails: Optional[List[str]] = None,
    bcc_emails: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Função helper para enviar email usando template do SendGrid
    
    Args:
        to_emails: Lista de emails destinatários
        template_id: ID do template dinâmico do SendGrid
        dynamic_template_data: Dados para preencher o template
        from_email: Email remetente
        from_name: Nome do remetente
        cc_emails: Lista de emails em cópia
        bcc_emails: Lista de emails em cópia oculta
        
    Returns:
        Dict com resultado do envio
    """
    email_service = get_email_service()
    return email_service.send_template_email(
        to_emails=to_emails,
        template_id=template_id,
        dynamic_template_data=dynamic_template_data,
        from_email=from_email,
        from_name=from_name,
        cc_emails=cc_emails,
        bcc_emails=bcc_emails
    )

