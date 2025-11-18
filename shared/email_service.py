"""
Serviço de email compartilhado usando SendGrid
"""
import os
from typing import List, Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
import base64
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    """Serviço para envio de emails via SendGrid"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o serviço de email
        
        Args:
            api_key: Chave API do SendGrid. Se não fornecida, será lida de SENDGRID_API_KEY
        """
        self.api_key = api_key or os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError(
                "SENDGRID_API_KEY não encontrada. "
                "Configure a variável de ambiente SENDGRID_API_KEY ou passe api_key no construtor."
            )
        self.client = SendGridAPIClient(self.api_key)
        self.default_from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@example.com')
        self.default_from_name = os.getenv('SENDGRID_FROM_NAME', 'NPS Surveys')
    
    def send_email(
        self,
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
        Envia um email via SendGrid
        
        Args:
            to_emails: Lista de emails destinatários
            subject: Assunto do email
            html_content: Conteúdo HTML do email
            text_content: Conteúdo texto do email (fallback se HTML não disponível)
            from_email: Email remetente (usa padrão se não fornecido)
            from_name: Nome do remetente (usa padrão se não fornecido)
            cc_emails: Lista de emails em cópia
            bcc_emails: Lista de emails em cópia oculta
            attachments: Lista de anexos no formato [{"filename": "file.pdf", "content": bytes, "type": "application/pdf"}]
            reply_to: Email para resposta
            categories: Categorias para tracking no SendGrid
            
        Returns:
            Dict com status_code e headers da resposta
            
        Raises:
            Exception: Se houver erro no envio
        """
        if not html_content and not text_content:
            raise ValueError("É necessário fornecer html_content ou text_content")
        
        from_email = from_email or self.default_from_email
        from_name = from_name or self.default_from_name
        
        # Criar objeto Mail
        message = Mail(
            from_email=Email(from_email, from_name),
            to_emails=[To(email) for email in to_emails],
            subject=subject
        )
        
        # Adicionar conteúdo
        if html_content:
            message.add_content(Content("text/html", html_content))
        if text_content:
            message.add_content(Content("text/plain", text_content))
        
        # Adicionar CC
        if cc_emails:
            for email in cc_emails:
                message.add_cc(Email(email))
        
        # Adicionar BCC
        if bcc_emails:
            for email in bcc_emails:
                message.add_bcc(Email(email))
        
        # Adicionar Reply-To
        if reply_to:
            message.reply_to = Email(reply_to)
        
        # Adicionar anexos
        if attachments:
            for attachment in attachments:
                file_content = attachment.get('content')
                if isinstance(file_content, bytes):
                    encoded_content = base64.b64encode(file_content).decode()
                elif isinstance(file_content, str):
                    encoded_content = base64.b64encode(file_content.encode()).decode()
                else:
                    raise ValueError("Conteúdo do anexo deve ser bytes ou string")
                
                attachment_obj = Attachment(
                    FileContent(encoded_content),
                    FileName(attachment.get('filename', 'attachment')),
                    FileType(attachment.get('type', 'application/octet-stream')),
                    Disposition(attachment.get('disposition', 'attachment'))
                )
                message.add_attachment(attachment_obj)
        
        # Adicionar categorias
        if categories:
            message.category = categories
        
        # Enviar email
        try:
            response = self.client.send(message)
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'success': 200 <= response.status_code < 300
            }
        except Exception as e:
            raise Exception(f"Erro ao enviar email: {str(e)}")
    
    def send_template_email(
        self,
        to_emails: List[str],
        template_id: str,
        dynamic_template_data: Dict[str, Any],
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Envia email usando template dinâmico do SendGrid
        
        Args:
            to_emails: Lista de emails destinatários
            template_id: ID do template dinâmico do SendGrid
            dynamic_template_data: Dados para preencher o template
            from_email: Email remetente
            from_name: Nome do remetente
            cc_emails: Lista de emails em cópia
            bcc_emails: Lista de emails em cópia oculta
            
        Returns:
            Dict com status_code e headers da resposta
        """
        from_email = from_email or self.default_from_email
        from_name = from_name or self.default_from_name
        
        message = Mail(
            from_email=Email(from_email, from_name),
            to_emails=[To(email) for email in to_emails]
        )
        
        message.template_id = template_id
        message.dynamic_template_data = dynamic_template_data
        
        if cc_emails:
            for email in cc_emails:
                message.add_cc(Email(email))
        
        if bcc_emails:
            for email in bcc_emails:
                message.add_bcc(Email(email))
        
        try:
            response = self.client.send(message)
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'success': 200 <= response.status_code < 300
            }
        except Exception as e:
            raise Exception(f"Erro ao enviar email com template: {str(e)}")


# Instância global (opcional, para uso direto)
_email_service_instance = None


def get_email_service() -> EmailService:
    """Retorna uma instância singleton do EmailService"""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance


