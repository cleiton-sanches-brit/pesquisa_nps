# Relatório do Estado Atual do Projeto – Pesquisa NPS

**Data do relatório:** Fevereiro 2025  
**Repositório:** https://github.com/cleiton-sanches-brit/pesquisa_nps

---

## 1. Visão geral

O **Sistema de Pesquisas NPS** é uma aplicação web para coleta e análise de pesquisas NPS (Net Promoter Score), com envio de convites por e-mail, formulários de resposta, dashboard de métricas e exportação de dados. O projeto está preparado para desenvolvimento local (SQLite) e produção (Azure SQL + Azure App Service).

---

## 2. Tecnologias implantadas

### 2.1 Backend e framework principal

| Tecnologia | Versão | Uso no projeto |
|------------|--------|----------------|
| **Python** | 3.12 (runtime.txt) | Linguagem base |
| **Django** | 4.2.7 | Framework web, admin, ORM, autenticação |
| **Django REST Framework** | 3.14.0 | API REST (surveys, responses) |
| **Gunicorn** | 21.2.0 | Servidor WSGI em produção |
| **python-dotenv** | 1.0.0 | Variáveis de ambiente (.env) |
| **django-environ** | 0.11.2 | Configuração via ambiente |

### 2.2 Banco de dados

| Tecnologia | Uso |
|------------|-----|
| **SQLite** | Desenvolvimento local (`USE_SQLITE=true`) |
| **Azure SQL / SQL Server** | Produção (ODBC Driver 17) |
| **django-pyodbc-azure** | 2.1.0.17 – backend Django para SQL Server |
| **pyodbc** | 5.0.1 – driver ODBC para SQL Server |
| **psycopg2-binary** | 2.9.9 – PostgreSQL (opcional, ex.: Supabase) |
| **SQLAlchemy** | 2.0.23 – uso auxiliar se necessário |

### 2.3 E-mail

| Tecnologia | Uso |
|------------|-----|
| **SendGrid** | 6.11.0 – envio de convites via API |
| **Backend customizado** | `surveys.email_backend.SendGridEmailBackend` |
| **Fallback** | SMTP (Django) quando SendGrid não está configurado |

### 2.4 Frontend e estáticos

| Tecnologia | Uso |
|------------|-----|
| **Django Templates** | HTML (templates em `django_app/templates/surveys/`) |
| **WhiteNoise** | 6.6.0 – servir estáticos em produção |
| **Plotly** | 5.17.0 – gráficos no dashboard NPS |

### 2.5 Segurança e rede

| Tecnologia | Uso |
|------------|-----|
| **django-cors-headers** | 4.3.1 – CORS para APIs/frontend |
| **cryptography** | 42.0.8 – criptografia |
| **Rate limiting** | Middleware customizado (`surveys.middleware.RateLimitMiddleware`) |
| **Proteção anti-spam** | Middleware customizado (`surveys.middleware.SpamProtectionMiddleware`) |
| **CSRF / Session** | Configurações Django (cookie secure, SameSite, etc.) |

### 2.6 Exportação e dados

| Tecnologia | Uso |
|------------|-----|
| **pandas** | 2.1.4 – manipulação de dados |
| **openpyxl** | 3.1.2 – exportação Excel |
| **WeasyPrint** | 60.2 – preview/export de conteúdo (ex.: e-mails) |

### 2.7 Deploy e infraestrutura

| Tecnologia | Uso |
|------------|-----|
| **Azure App Service** | Hospedagem em produção |
| **GitHub Actions** | CI/CD (workflows em `.github/workflows/`) |
| **Docker** | Dockerfile em `django_app/` (Python 3.11-slim, ODBC) |
| **Procfile** | Comando de start (migrate, collectstatic, gunicorn) |
| **startup.sh** | Script de inicialização no Azure (migrate, collectstatic, Gunicorn) |

### 2.8 Desenvolvimento e testes

| Tecnologia | Uso |
|------------|-----|
| **pytest** | 7.4.3 – testes |
| **pytest-django** | 4.7.0 – integração Django |
| **black** | 23.11.0 – formatação |
| **flake8** | 6.1.0 – lint |

### 2.9 Outras dependências

- **FastAPI / Uvicorn / Pydantic** – presentes no `requirements.txt` (uso específico, se houver, em outros módulos).
- **requests** – chamadas HTTP.
- **email-validator** – validação de e-mail.

---

## 3. Estrutura do projeto

```
pesquisa_nps/
├── django_app/                    # Aplicação Django
│   ├── nps_admin/                 # Configurações do projeto
│   │   ├── settings.py            # Settings (DB, email, CORS, cache, REST)
│   │   ├── urls.py                # URLs principais + redirect raiz → admin
│   │   ├── wsgi.py / asgi.py
│   │   └── __init__.py
│   ├── surveys/                   # App de pesquisas NPS
│   │   ├── models.py              # Survey, Respondent, SurveyInvitation, Question, Answer, etc.
│   │   ├── views.py               # ViewSets REST (surveys, responses)
│   │   ├── views_invitations.py   # Convites e respostas
│   │   ├── views_nps.py           # Dashboard NPS, exportação
│   │   ├── views_selecao.py       # Lista de convidados
│   │   ├── views_tracking.py      # Tracking de e-mail (abertura/clique)
│   │   ├── urls.py / urls_*.py    # Rotas da app
│   │   ├── admin.py               # Registro no Django Admin
│   │   ├── middleware.py         # Rate limit + anti-spam
│   │   ├── email_backend.py       # SendGrid
│   │   ├── security.py
│   │   ├── serializers.py
│   │   └── management/commands/   # criar_lista_convidados
│   ├── templates/surveys/         # Templates HTML
│   ├── manage.py
│   ├── Dockerfile
│   └── (migrations)
├── .github/workflows/             # GitHub Actions (Azure deploy, homolog)
├── requirements.txt
├── runtime.txt                    # python-3.12.0
├── Procfile
├── startup.sh
├── env.example / env_azure_example
├── INICIAR_SERVIDOR_ADRIANO.bat   # Script local Windows
├── criar_admin_azure.py           # Criação de superusuário
└── Documentação (.md / .txt)
```

---

## 4. Funcionalidades implementadas

### 4.1 Administração (Django Admin)

- Gestão de **Pesquisas** (Survey): título, descrição, ativa, expiração, múltiplas respostas.
- Gestão de **Respondentes** (Respondent): e-mail, nome, conta, produto, status.
- Gestão de **Convites** (SurveyInvitation) e envio por e-mail.
- Visualização de **respostas** e **questões**.

### 4.2 Convites e respostas

- Envio de convites por e-mail (SendGrid).
- Formulário de resposta por link único (`/survey/<id>/respond/<token>/`).
- Lista de convites por pesquisa, reenvio de convite.
- Criação de lista de convidados e preview de seleção.

### 4.3 NPS

- Dashboard NPS (`/nps/dashboard/`, `/nps/dashboard/<id>/`).
- Cálculo de NPS por período.
- Exportação Excel e CSV.
- API de dados para gráficos (Plotly).

### 4.4 Tracking de e-mail

- Registro de abertura e clique no link (pixel e redirect).
- Estatísticas e detalhes por pesquisa.

### 4.5 API REST

- Endpoints para surveys e responses (DRF).
- Throttling (anon/user).
- Autenticação para recursos protegidos.

### 4.6 Segurança e UX

- Rate limiting e proteção anti-spam.
- Bloqueio de múltiplas respostas (configurável por pesquisa).
- Pesquisa expirada e telas de feedback (obrigado, já respondido, bloqueado).

---

## 5. Ambientes suportados

| Ambiente | Banco | Observação |
|----------|--------|------------|
| **Local (dev)** | SQLite | `USE_SQLITE=true`; script `INICIAR_SERVIDOR_ADRIANO.bat` |
| **Produção** | Azure SQL | Variáveis `DB_*`; ODBC Driver 17 |
| **Azure App Service** | Azure SQL | Deploy via GitHub Actions; `startup.sh` + Gunicorn |
| **Railway** | Opcional | `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` suportam `RAILWAY_PUBLIC_DOMAIN` |

---

## 6. URLs principais

| URL | Descrição |
|-----|-----------|
| `/` | Redireciona para `/admin/` |
| `/admin/` | Interface administrativa Django |
| `/api/` | API REST (surveys, responses) |
| `/survey/<id>/invite/` | Envio de convites |
| `/survey/<id>/respond/<token>/` | Formulário de resposta |
| `/survey/<id>/invitations/` | Lista de convites |
| `/nps/dashboard/` | Dashboard NPS |
| `/nps/export/<id>/excel/` e `.../csv/` | Exportação |
| `/track/email/open/<token>/`, `/track/link/click/<token>/` | Tracking de e-mail |

---

## 7. Resumo executivo

- **Stack:** Python 3.12, Django 4.2, DRF, SQLite (local) / Azure SQL (produção), SendGrid, WhiteNoise, Gunicorn.
- **Deploy:** Azure App Service com GitHub Actions; Docker e Procfile/startup.sh disponíveis.
- **Segurança:** CORS, rate limit, anti-spam, CSRF, cookies seguros, throttling na API.
- **Estado:** Projeto funcional para desenvolvimento local e preparado para produção no Azure, com documentação e scripts de inicialização e criação de usuário admin.

---

*Relatório gerado com base no código e configurações do repositório pesquisa_nps.*
