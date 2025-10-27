# Survey Analytics

Sistema híbrido para coleta e análise de pesquisas NPS, CSAT e CES utilizando Django para administração e FastAPI para coleta de respostas.

## 🏗️ Arquitetura

- **Django**: Painel administrativo, relatórios, visualizações e exportações
- **FastAPI**: Coleta de respostas via endpoints públicos (API)
- **Banco de Dados**: SQL Server (banco único para ambas as aplicações)
- **Versionamento**: GitHub

## 📁 Estrutura do Projeto

```
survey_analytics/
├── dashboard/                 # Aplicação Django (Painel Admin)
│   ├── survey_analytics/     # Configurações do projeto Django
│   ├── dashboard/            # App de dashboard
│   │   ├── models.py         # Modelos de dados (Customer, Survey, Response)
│   │   ├── admin.py          # Interface administrativa
│   │   ├── views.py          # Views do dashboard e relatórios
│   │   ├── urls.py           # URLs do dashboard
│   │   └── templates/        # Templates HTML com Bootstrap e Chart.js
│   └── manage.py
├── collector/                # Aplicação FastAPI (Coleta)
│   ├── api/                  # Endpoints REST
│   │   └── nps.py           # Endpoints NPS (/api/nps/submit, /results, /summary)
│   ├── schemas/             # Schemas Pydantic e Modelos SQLAlchemy
│   ├── crud/                # Operações CRUD
│   ├── main.py              # Aplicação principal FastAPI
│   └── database.py          # Configuração do banco
├── database/                # Scripts de banco
├── scripts/                 # Scripts utilitários
├── docs/                    # Documentação
├── requirements.txt         # Dependências Python
├── docker-compose.yml       # Orquestração de containers
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
cd survey_analytics
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
DB_NAME=survey_analytics
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
```

### 5. Configure o banco de dados

1. Crie o banco de dados `survey_analytics` no SQL Server
2. Execute as migrações do Django:

```bash
cd dashboard
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Execute as aplicações

#### Django (Dashboard - Porta 8000)
```bash
cd dashboard
python manage.py runserver
```

#### FastAPI (Collector - Porta 8001)
```bash
cd collector
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

### FastAPI Collector (http://localhost:8001)

#### NPS
- `POST /api/nps/submit` - Enviar resposta NPS
- `GET /api/nps/results` - Listar resultados NPS
- `GET /api/nps/summary` - Resumo agregado NPS

### Django Dashboard (http://localhost:8000)

#### Dashboard
- `GET /` - Dashboard principal com gráficos
- `GET /surveys/` - Lista de pesquisas
- `GET /responses/` - Lista de respostas com filtros
- `GET /export/csv/` - Exportar CSV
- `GET /export/excel/` - Exportar Excel
- `GET /admin/` - Interface administrativa

## 📝 Exemplo de Uso

### Enviar Resposta NPS via FastAPI

```bash
curl -X POST "http://localhost:8001/api/nps/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "João Silva",
    "customer_email": "joao@example.com",
    "customer_company": "Empresa ABC",
    "survey_id": 1,
    "score": 9,
    "comment": "Excelente atendimento!"
  }'
```

### Obter Resumo NPS via FastAPI

```bash
curl -X GET "http://localhost:8001/api/nps/summary"
```

## 🧪 Testes

```bash
# Testes Django
cd dashboard
python manage.py test

# Testes FastAPI
cd collector
pytest
```

## 📈 Monitoramento

- **Django Dashboard**: http://localhost:8000/
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
