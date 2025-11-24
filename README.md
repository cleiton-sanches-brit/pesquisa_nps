# Sistema de Pesquisas NPS

Sistema Django para coleta e análise de pesquisas NPS (Net Promoter Score) com envio automático de convites por email via SendGrid.

## 🏗️ Arquitetura

- **Django**: Aplicação web completa para administração, envio de convites e coleta de respostas
- **Banco de Dados**: Azure SQL Database
- **Email**: SendGrid API para envio de convites
- **Deploy**: Pronto para Azure App Service

## 📁 Estrutura do Projeto

```
pesquisas_nps/
├── django_app/                 # Aplicação Django
│   ├── nps_admin/              # Configurações do projeto Django
│   ├── surveys/                # App principal de pesquisas
│   │   ├── models.py           # Modelos (Survey, SurveyInvitation, Respondent)
│   │   ├── views.py            # Views principais
│   │   ├── views_invitations.py # Views de convites
│   │   ├── views_nps.py        # Views do dashboard NPS
│   │   ├── urls.py             # URLs principais
│   │   └── migrations/         # Migrações do banco de dados
│   ├── templates/              # Templates HTML
│   └── manage.py               # Script de gerenciamento Django
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão do Python
├── Procfile                    # Configuração para deploy
├── .env                        # Variáveis de ambiente (não versionado)
└── README.md                   # Este arquivo
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- Azure SQL Database (ou SQL Server)
- Conta SendGrid para envio de emails
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/cleiton-sanches-brit/pesquisa_nps.git
cd pesquisas_nps
```

### 2. Configure o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure:

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Django Settings
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (Azure SQL)
DB_HOST=seu-servidor-azure.database.windows.net
DB_PORT=1433
DB_NAME=dbNPS
DB_USER=seu-usuario
DB_PASSWORD=sua-senha

# SendGrid Email
SENDGRID_API_KEY=sua-api-key-sendgrid
SENDGRID_FROM_EMAIL=no-reply@br-itsoftware.com.br

# CSRF Settings
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com
```

### 5. Configure o banco de dados

1. Crie o banco de dados no Azure SQL Database
2. Execute as migrações:

```bash
cd django_app
python manage.py migrate
python manage.py createsuperuser
```

### 6. Execute a aplicação

```bash
cd django_app
python manage.py runserver
```

A aplicação estará disponível em: `http://localhost:8000`

## 📊 Funcionalidades

### Administração Django
- **Gestão de Pesquisas**: Criar, editar e gerenciar pesquisas NPS
- **Envio de Convites**: Enviar convites por email via SendGrid
- **Visualização de Respostas**: Ver todas as respostas coletadas
- **Dashboard NPS**: Calcular e visualizar scores NPS
- **Exportação de Dados**: Exportar dados em Excel/CSV

### Formulário de Resposta
- Formulário público para responder pesquisas
- Proteção contra spam e múltiplas respostas
- Tracking de abertura e cliques em emails

## 🔗 URLs Principais

- `/admin/` - Interface administrativa Django
- `/survey/<id>/respond/<token>/` - Formulário de resposta
- `/nps/dashboard/` - Dashboard NPS
- `/nps/export/` - Exportação de dados

## 🚀 Deploy no Azure

O projeto está configurado para deploy no Azure App Service:

1. Configure as variáveis de ambiente no Azure Portal
2. Configure o banco de dados Azure SQL
3. Configure o SendGrid para envio de emails
4. Faça o deploy via GitHub Actions ou Azure CLI

## 📝 Variáveis de Ambiente para Produção

```env
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,*.azurewebsites.net
SECRET_KEY=chave-secreta-forte
DB_HOST=seu-servidor-azure.database.windows.net
DB_NAME=dbNPS
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
SENDGRID_API_KEY=sua-api-key
SENDGRID_FROM_EMAIL=no-reply@br-itsoftware.com.br
CSRF_TRUSTED_ORIGINS=https://seu-dominio.com
```

## 📄 Licença

Este projeto está sob a licença MIT.
