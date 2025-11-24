"""
Backend customizado do Django para envio de emails via SendGrid API
"""
import os
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.conf import settings
import sys
from pathlib import Path

# Adicionar o diretório shared ao path
project_root = Path(__file__).resolve().parent.parent.parent.parent
shared_path = project_root / "shared"
sys.path.insert(0, str(shared_path))

from shared.email_service import EmailService


class SendGridEmailBackend(BaseEmailBackend):
    """
    Backend do Django para envio de emails via SendGrid API
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            if not self.fail_silently:
                raise ValueError(
                    "SENDGRID_API_KEY não encontrada. "
                    "Configure a variável de ambiente SENDGRID_API_KEY."
                )
            self.email_service = None
        else:
            try:
                self.email_service = EmailService(api_key=self.api_key)
            except Exception as e:
                if not self.fail_silently:
                    raise
                self.email_service = None
    
    def send_messages(self, email_messages):
        """
        Envia uma ou mais mensagens de email via SendGrid
        """
        if not self.email_service:
            return 0
        
        num_sent = 0
        for message in email_messages:
            try:
                # Extrair informações do EmailMessage
                to_emails = message.to
                subject = message.subject
                
                # Extrair conteúdo HTML e texto
                html_content = None
                text_content = None
                
                if isinstance(message, EmailMultiAlternatives):
                    # Verificar alternativas (HTML/texto)
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            html_content = content
                        elif mimetype == 'text/plain':
                            text_content = content
                
                # Se não tiver HTML, usar o corpo da mensagem como texto
                if not html_content and not text_content:
                    text_content = message.body
                elif not text_content:
                    # Se só tiver HTML, criar versão texto simples
                    text_content = message.body or "Email HTML - visualize em cliente compatível"
                
                # Obter remetente
                from_email = message.from_email or os.getenv('SENDGRID_FROM_EMAIL', 'no-reply@m4law.com.br')
                from_name = os.getenv('SENDGRID_FROM_NAME', 'M4Law')
                
                # Extrair CC e BCC
                cc_emails = message.cc if hasattr(message, 'cc') and message.cc else None
                bcc_emails = message.bcc if hasattr(message, 'bcc') and message.bcc else None
                
                # Extrair reply-to
                reply_to = None
                if hasattr(message, 'reply_to') and message.reply_to:
                    reply_to = message.reply_to[0] if isinstance(message.reply_to, list) else message.reply_to
                
                # Enviar via SendGrid
                result = self.email_service.send_email(
                    to_emails=to_emails,
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content,
                    from_email=from_email,
                    from_name=from_name,
                    cc_emails=cc_emails,
                    bcc_emails=bcc_emails,
                    reply_to=reply_to
                )
                
                if result.get('success'):
                    num_sent += 1
                else:
                    if not self.fail_silently:
                        raise Exception(f"Falha ao enviar email: Status {result.get('status_code')}")
            
            except Exception as e:
                if not self.fail_silently:
                    raise
                # Em modo fail_silently, apenas continua para o próximo email
        
        return num_sent


