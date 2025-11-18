"""
Exemplos práticos de uso do serviço de email SendGrid
"""
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

# Exemplo 1: Envio simples de email
def exemplo_envio_simples():
    """Exemplo básico de envio de email"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    try:
        result = email_service.send_email(
            to_emails=["exemplo@teste.com"],
            subject="Teste de Email - Pesquisa NPS",
            html_content="""
            <html>
                <body>
                    <h1 style="color: #4CAF50;">Olá!</h1>
                    <p>Este é um email de teste do sistema de pesquisas NPS.</p>
                    <p>Obrigado por participar!</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        Este é um email automático, por favor não responda.
                    </p>
                </body>
            </html>
            """,
            text_content="Olá! Este é um email de teste do sistema de pesquisas NPS."
        )
        
        print(f"✅ Email enviado com sucesso!")
        print(f"   Status Code: {result['status_code']}")
        return result
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return None


# Exemplo 2: Email com múltiplos destinatários e cópias
def exemplo_email_multiplos_destinatarios():
    """Exemplo de email com CC e BCC"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    try:
        result = email_service.send_email(
            to_emails=["cliente@example.com"],
            subject="Relatório de Pesquisas NPS",
            html_content="""
            <h1>Relatório de Pesquisas</h1>
            <p>Segue o relatório mensal de pesquisas NPS.</p>
            <ul>
                <li>Total de respostas: 150</li>
                <li>NPS Score: 45</li>
                <li>Taxa de resposta: 30%</li>
            </ul>
            """,
            cc_emails=["gerente@example.com"],
            bcc_emails=["admin@example.com"],
            reply_to="suporte@example.com"
        )
        
        print(f"✅ Email enviado para múltiplos destinatários!")
        return result
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


# Exemplo 3: Email com anexo
def exemplo_email_com_anexo():
    """Exemplo de email com anexo PDF"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    # Simular conteúdo de um PDF (em produção, ler de arquivo real)
    pdf_content = b"%PDF-1.4\n%Exemplo de PDF\n"
    
    try:
        result = email_service.send_email(
            to_emails=["admin@example.com"],
            subject="Relatório PDF - Pesquisas NPS",
            html_content="<p>Segue em anexo o relatório em PDF.</p>",
            attachments=[{
                "filename": "relatorio_nps.pdf",
                "content": pdf_content,
                "type": "application/pdf",
                "disposition": "attachment"
            }]
        )
        
        print(f"✅ Email com anexo enviado!")
        return result
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


# Exemplo 4: Email usando template dinâmico
def exemplo_email_template():
    """Exemplo de email usando template do SendGrid"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    # Substitua pelo ID do seu template no SendGrid
    template_id = "d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    try:
        result = email_service.send_template_email(
            to_emails=["cliente@example.com"],
            template_id=template_id,
            dynamic_template_data={
                "nome": "João Silva",
                "empresa": "Minha Empresa",
                "link_pesquisa": "https://example.com/pesquisa/123",
                "data_vencimento": "31/12/2024"
            }
        )
        
        print(f"✅ Email com template enviado!")
        return result
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


# Exemplo 5: Notificação quando pesquisa é respondida
def exemplo_notificacao_resposta(survey_id: int, respondent_email: str, nps_score: int):
    """Exemplo de notificação quando uma pesquisa é respondida"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    # Determinar categoria baseada no NPS
    if nps_score >= 9:
        categoria = "Promotor"
        cor = "#4CAF50"
        mensagem = "Excelente! Você é um promotor da nossa marca!"
    elif nps_score >= 7:
        categoria = "Neutro"
        cor = "#FF9800"
        mensagem = "Obrigado pelo seu feedback!"
    else:
        categoria = "Detrator"
        cor = "#F44336"
        mensagem = "Obrigado pelo feedback. Vamos melhorar!"
    
    try:
        result = email_service.send_email(
            to_emails=[respondent_email],
            subject="Obrigado pela sua resposta!",
            html_content=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: {cor};">Obrigado pela sua participação!</h1>
                        <p>Olá,</p>
                        <p>Sua resposta foi registrada com sucesso.</p>
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Pesquisa ID:</strong> {survey_id}</p>
                            <p><strong>Seu NPS:</strong> {nps_score}/10</p>
                            <p><strong>Categoria:</strong> {categoria}</p>
                        </div>
                        <p>{mensagem}</p>
                        <p>Seu feedback é muito importante para nós.</p>
                        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            Este é um email automático. Por favor, não responda.
                        </p>
                    </div>
                </body>
            </html>
            """,
            text_content=f"""
            Obrigado pela sua participação!
            
            Pesquisa ID: {survey_id}
            Seu NPS: {nps_score}/10
            Categoria: {categoria}
            
            {mensagem}
            """,
            categories=["nps", "notification", "survey_response"]
        )
        
        print(f"✅ Notificação enviada para {respondent_email}!")
        return result
    except Exception as e:
        print(f"❌ Erro ao enviar notificação: {e}")
        return None


# Exemplo 6: Relatório semanal para administradores
def exemplo_relatorio_semanal(admin_emails: list, dados_relatorio: dict):
    """Exemplo de envio de relatório semanal"""
    from shared.email_service import EmailService
    
    email_service = EmailService()
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                <h1>Relatório Semanal de Pesquisas NPS</h1>
                <p>Período: {dados_relatorio.get('periodo', 'N/A')}</p>
                
                <h2>Resumo</h2>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr style="background-color: #f5f5f5;">
                        <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Métrica</th>
                        <th style="padding: 10px; text-align: right; border: 1px solid #ddd;">Valor</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;">Total de Respostas</td>
                        <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{dados_relatorio.get('total_respostas', 0)}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;">NPS Score</td>
                        <td style="padding: 10px; text-align: right; border: 1px solid #ddd; font-weight: bold;">{dados_relatorio.get('nps_score', 0)}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;">Taxa de Resposta</td>
                        <td style="padding: 10px; text-align: right; border: 1px solid #ddd;">{dados_relatorio.get('taxa_resposta', 0)}%</td>
                    </tr>
                </table>
                
                <h2>Distribuição</h2>
                <ul>
                    <li>Promotores: {dados_relatorio.get('promotores', 0)}</li>
                    <li>Neutros: {dados_relatorio.get('neutros', 0)}</li>
                    <li>Detratores: {dados_relatorio.get('detratores', 0)}</li>
                </ul>
            </div>
        </body>
    </html>
    """
    
    try:
        result = email_service.send_email(
            to_emails=admin_emails,
            subject=f"Relatório Semanal NPS - {dados_relatorio.get('periodo', '')}",
            html_content=html_content,
            categories=["nps", "report", "weekly"]
        )
        
        print(f"✅ Relatório enviado para {len(admin_emails)} administrador(es)!")
        return result
    except Exception as e:
        print(f"❌ Erro ao enviar relatório: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("Exemplos de Uso do Serviço de Email SendGrid")
    print("=" * 60)
    print()
    
    # Verificar se a API key está configurada
    if not os.getenv('SENDGRID_API_KEY'):
        print("⚠️  AVISO: SENDGRID_API_KEY não encontrada no .env")
        print("   Configure a variável antes de executar os exemplos.")
        print()
    
    # Descomente o exemplo que deseja testar:
    
    # exemplo_envio_simples()
    # exemplo_email_multiplos_destinatarios()
    # exemplo_email_com_anexo()
    # exemplo_email_template()
    # exemplo_notificacao_resposta(123, "cliente@example.com", 8)
    # exemplo_relatorio_semanal(
    #     ["admin@example.com"],
    #     {
    #         "periodo": "01/01/2024 - 07/01/2024",
    #         "total_respostas": 150,
    #         "nps_score": 45,
    #         "taxa_resposta": 30,
    #         "promotores": 60,
    #         "neutros": 50,
    #         "detratores": 40
    #     }
    # )


