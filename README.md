# Sistema de Pesquisas NPS

Sistema híbrido para coleta e análise de pesquisas NPS (Net Promoter Score) utilizando Django para administração e FastAPI para coleta de respostas.

## 🏗️ Arquitetura

- **Django**: Painel administrativo, relatórios, visualizações e exportações
- **FastAPI**: Coleta de respostas via endpoints públicos (API)
- **Banco de Dados**: SQL Server (banco único para ambas as aplicações)
- **Versionamento**: GitHub

## 📁 Estrutura do Projeto

```
pesquisas_nps/
├── django_app/                 # Aplicação Django
│   ├── nps_admin/             # Configurações do projeto Django
│   ├── surveys/               # App de pesquisas
│   │   ├── models.py          # Modelos de dados
│   │   ├── admin.py           # Interface administrativa
│   │   ├── serializers.py     # Serializers para API REST
│   │   ├── views.py           # Views da API REST
│   │   └── urls.py            # URLs da API
│   └── manage.py
├── fastapi_app/               # Aplicação FastAPI
│   ├── routers/               # Routers da API
│   ├── main.py                # Aplicação principal
│   ├── models.py              # Modelos SQLAlchemy
│   ├── schemas.py             # Schemas Pydantic
│   └── database.py            # Configuração do banco
├── shared/                    # Código compartilhado
├── database/                  # Scripts de banco
├── migrations/                # Migrações
├── scripts/                   # Scripts utilitários
├── docs/                      # Documentação
├── requirements.txt           # Dependências Python
├── docker-compose.yml         # Orquestração de containers
└── README.md
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- SQL Server 2019+
- Git

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
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

# Database Settings
DB_HOST=localhost
DB_PORT=1433
DB_NAME=nps_surveys
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
```

### 5. Configure o banco de dados

1. Crie o banco de dados `nps_surveys` no SQL Server
2. Execute as migrações do Django:

```bash
cd django_app
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Execute as aplicações

#### Django (Admin - Porta 8000)
```bash
cd django_app
python manage.py runserver
```

#### FastAPI (API - Porta 8001)
```bash
cd fastapi_app
uvicorn main:app --reload --port 8001
```

## 🐳 Execução com Docker

### Usando Docker Compose

```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## 📊 Funcionalidades

### Django Admin (Porta 8000)
- **Gestão de Pesquisas**: Criar, editar e gerenciar pesquisas NPS
- **Gestão de Perguntas**: Configurar perguntas e opções
- **Visualização de Respostas**: Ver todas as respostas coletadas
- **Relatórios NPS**: Calcular e visualizar scores NPS
- **Exportação de Dados**: Exportar dados em Excel/CSV

### FastAPI (Porta 8001)
- **Coleta de Respostas**: Endpoints públicos para receber respostas
- **Validação de Dados**: Validação automática de respostas
- **API RESTful**: Interface completa para integração

## 🔗 Endpoints da API

### FastAPI (http://localhost:8001)

#### Pesquisas
- `GET /api/v1/surveys` - Listar pesquisas ativas
- `GET /api/v1/surveys/{id}` - Obter pesquisa específica

#### Respostas
- `POST /api/v1/responses` - Enviar resposta de pesquisa
- `GET /api/v1/responses` - Listar respostas (admin)
- `GET /api/v1/surveys/{id}/responses` - Respostas de uma pesquisa

### Django REST (http://localhost:8000)

#### Pesquisas
- `GET /api/surveys/` - Listar pesquisas
- `POST /api/surveys/` - Criar pesquisa
- `GET /api/surveys/{id}/responses/` - Respostas de uma pesquisa
- `POST /api/surveys/{id}/calculate_nps/` - Calcular NPS

## 📝 Exemplo de Uso

### Enviar Resposta via FastAPI

```bash
curl -X POST "http://localhost:8001/api/v1/responses" \
  -H "Content-Type: application/json" \
  -d '{
    "survey_id": 1,
    "respondent_id": "user123",
    "respondent_email": "user@example.com",
    "answers": [
      {
        "question_id": 1,
        "answer_value": "9"
      },
      {
        "question_id": 2,
        "answer_text": "Excelente atendimento!"
      }
    ]
  }'
```

### Calcular NPS via Django

```bash
curl -X POST "http://localhost:8000/api/surveys/1/calculate_nps/" \
  -H "Content-Type: application/json" \
  -d '{
    "period_start": "2024-01-01",
    "period_end": "2024-01-31"
  }'
```

## 🧪 Testes

```bash
# Testes Django
cd django_app
python manage.py test

# Testes FastAPI
cd fastapi_app
pytest
```

## 📈 Monitoramento

- **Django Admin**: http://localhost:8000/admin/
- **FastAPI Docs**: http://localhost:8001/docs
- **FastAPI ReDoc**: http://localhost:8001/redoc

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através de:
- Email: suporte@exemplo.com
- Issues: [GitHub Issues](https://github.com/seu-usuario/pesquisas_nps/issues)
