"""
Script para criar tabelas diretamente no SQL Server usando SQL puro
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pyodbc

load_dotenv()

def conectar_banco():
    """Conecta ao banco SQL Server"""
    db_host = os.getenv('DB_HOST', '172.190.157.142')
    db_port = os.getenv('DB_PORT', '1433')
    db_name = os.getenv('DB_NAME', 'dbNPS')
    db_user = os.getenv('DB_USER', 'user-nps')
    db_password = os.getenv('DB_PASSWORD', '')
    
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        f"TrustServerCertificate=yes;"
    )
    
    return pyodbc.connect(connection_string)


def criar_tabelas():
    """Cria as tabelas necessárias no banco"""
    print("="*60)
    print("Criando Tabelas no Azure SQL Server")
    print("="*60)
    print()
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        print("[OK] Conexao estabelecida!")
        print()
        
        # SQL para criar tabelas principais do Django
        # Começando com as tabelas do sistema Django
        print("1. Criando tabela de migracoes do Django...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'django_migrations')
            CREATE TABLE django_migrations (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                app nvarchar(255) NOT NULL,
                name nvarchar(255) NOT NULL,
                applied datetime2 NOT NULL
            )
        """)
        conn.commit()
        print("   [OK] Tabela django_migrations criada")
        print()
        
        # Tabela auth_user (usuários do Django)
        print("2. Criando tabela auth_user...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'auth_user')
            CREATE TABLE auth_user (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                password nvarchar(128) NOT NULL,
                last_login datetime2 NULL,
                is_superuser bit NOT NULL DEFAULT 0,
                username nvarchar(150) NOT NULL UNIQUE,
                first_name nvarchar(150) NOT NULL DEFAULT '',
                last_name nvarchar(150) NOT NULL DEFAULT '',
                email nvarchar(254) NOT NULL DEFAULT '',
                is_staff bit NOT NULL DEFAULT 0,
                is_active bit NOT NULL DEFAULT 1,
                date_joined datetime2 NOT NULL DEFAULT GETDATE()
            )
        """)
        conn.commit()
        print("   [OK] Tabela auth_user criada")
        print()
        
        # Tabela surveys_survey
        print("3. Criando tabela surveys_survey...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_survey')
            CREATE TABLE surveys_survey (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                title nvarchar(200) NOT NULL,
                description nvarchar(max) NULL,
                is_active bit NOT NULL DEFAULT 1,
                created_at datetime2 NOT NULL DEFAULT GETDATE(),
                updated_at datetime2 NOT NULL DEFAULT GETDATE(),
                created_by_id bigint NULL,
                expires_at datetime2 NULL,
                allow_multiple_responses bit NOT NULL DEFAULT 0,
                FOREIGN KEY (created_by_id) REFERENCES auth_user(id)
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_survey criada")
        print()
        
        # Tabela surveys_respondent
        print("4. Criando tabela surveys_respondent...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_respondent')
            CREATE TABLE surveys_respondent (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                email nvarchar(254) NOT NULL UNIQUE,
                nome_conta nvarchar(200) NOT NULL DEFAULT '',
                nome_usuario nvarchar(200) NOT NULL DEFAULT '',
                nome_produto nvarchar(200) NULL,
                status_usuario nvarchar(50) NOT NULL DEFAULT 'Ativo',
                notes nvarchar(max) NOT NULL DEFAULT '',
                active bit NOT NULL DEFAULT 1,
                created_at datetime2 NOT NULL DEFAULT GETDATE(),
                updated_at datetime2 NOT NULL DEFAULT GETDATE()
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_respondent criada")
        print()
        
        # Tabela surveys_question
        print("5. Criando tabela surveys_question...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_question')
            CREATE TABLE surveys_question (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                survey_id bigint NOT NULL,
                question_text nvarchar(max) NOT NULL,
                question_type nvarchar(10) NOT NULL,
                is_required bit NOT NULL DEFAULT 1,
                [order] int NOT NULL DEFAULT 0,
                created_at datetime2 NOT NULL DEFAULT GETDATE(),
                FOREIGN KEY (survey_id) REFERENCES surveys_survey(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_question criada")
        print()
        
        # Tabela surveys_choice
        print("6. Criando tabela surveys_choice...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_choice')
            CREATE TABLE surveys_choice (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                question_id bigint NOT NULL,
                choice_text nvarchar(200) NOT NULL,
                value nvarchar(50) NOT NULL,
                [order] int NOT NULL DEFAULT 0,
                FOREIGN KEY (question_id) REFERENCES surveys_question(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_choice criada")
        print()
        
        # Tabela surveys_surveyinvitation
        print("7. Criando tabela surveys_surveyinvitation...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_surveyinvitation')
            CREATE TABLE surveys_surveyinvitation (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                survey_id bigint NOT NULL,
                email nvarchar(254) NOT NULL,
                unique_token uniqueidentifier NOT NULL UNIQUE DEFAULT NEWID(),
                is_used bit NOT NULL DEFAULT 0,
                used_at datetime2 NULL,
                created_at datetime2 NOT NULL DEFAULT GETDATE(),
                expires_at datetime2 NOT NULL,
                sent_at datetime2 NULL,
                opened_at datetime2 NULL,
                clicked_at datetime2 NULL,
                open_count int NOT NULL DEFAULT 0,
                click_count int NOT NULL DEFAULT 0,
                FOREIGN KEY (survey_id) REFERENCES surveys_survey(id) ON DELETE CASCADE,
                UNIQUE (survey_id, email)
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_surveyinvitation criada")
        print()
        
        # Tabela surveys_surveyresponse
        print("8. Criando tabela surveys_surveyresponse...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_surveyresponse')
            CREATE TABLE surveys_surveyresponse (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                survey_id bigint NOT NULL,
                respondent_id nvarchar(100) NOT NULL,
                respondent_email nvarchar(255) NULL,
                submitted_at datetime2 NOT NULL DEFAULT GETDATE(),
                ip_address nvarchar(45) NULL,
                user_agent nvarchar(max) NULL,
                FOREIGN KEY (survey_id) REFERENCES surveys_survey(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_surveyresponse criada")
        print()
        
        # Tabela surveys_answer
        print("9. Criando tabela surveys_answer...")
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surveys_answer')
            CREATE TABLE surveys_answer (
                id bigint IDENTITY(1,1) PRIMARY KEY,
                response_id bigint NOT NULL,
                question_id bigint NOT NULL,
                answer_text nvarchar(max) NULL,
                answer_value nvarchar(100) NULL,
                answer_choice_id bigint NULL,
                created_at datetime2 NOT NULL DEFAULT GETDATE(),
                FOREIGN KEY (response_id) REFERENCES surveys_surveyresponse(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES surveys_question(id) ON DELETE NO ACTION,
                FOREIGN KEY (answer_choice_id) REFERENCES surveys_choice(id) ON DELETE NO ACTION
            )
        """)
        conn.commit()
        print("   [OK] Tabela surveys_answer criada")
        print()
        
        # Criar índices para melhor performance
        print("10. Criando indices...")
        try:
            cursor.execute("CREATE INDEX idx_survey_response_survey ON surveys_surveyresponse(survey_id)")
            cursor.execute("CREATE INDEX idx_question_survey ON surveys_question(survey_id)")
            cursor.execute("CREATE INDEX idx_answer_response ON surveys_answer(response_id)")
            cursor.execute("CREATE INDEX idx_answer_question ON surveys_answer(question_id)")
            conn.commit()
            print("   [OK] Indices criados")
        except Exception as e:
            print(f"   [AVISO] Alguns indices podem ja existir: {e}")
        print()
        
        # Verificar tabelas criadas
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tabelas = cursor.fetchall()
        
        print("="*60)
        print("RESUMO")
        print("="*60)
        print()
        print(f"Total de tabelas criadas: {len(tabelas)}")
        print()
        print("Tabelas no banco:")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        print()
        
        cursor.close()
        conn.close()
        
        print("[OK] Tabelas criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print()
    criar_tabelas()
    print()

