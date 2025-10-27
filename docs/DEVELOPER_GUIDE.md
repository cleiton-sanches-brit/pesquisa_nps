# 👨‍💻 Guia do Desenvolvedor - Survey Analytics

## 🏗️ Arquitetura do Sistema

### Visão Geral
O Survey Analytics é um sistema híbrido composto por:

1. **Django Dashboard** (`dashboard/`): Interface administrativa e relatórios
2. **FastAPI Collector** (`collector/`): API para coleta de respostas
3. **SQL Server**: Banco de dados compartilhado
4. **Templates HTML**: Interface web com Bootstrap e Chart.js

### Fluxo de Dados
```
Cliente → FastAPI Collector → SQL Server → Django Dashboard → Usuário Admin
```

## 📁 Estrutura Detalhada

### Django Dashboard (`dashboard/`)
```
dashboard/
├── survey_analytics/          # Configurações do projeto
│   ├── settings.py           # Configurações Django
│   ├── urls.py               # URLs principais
│   └── wsgi.py               # WSGI application
├── dashboard/                 # App principal
│   ├── models.py             # Modelos de dados (Customer, Survey, Response)
│   ├── views.py              # Views do dashboard e relatórios
│   ├── admin.py              # Interface administrativa
│   ├── urls.py               # URLs do app
│   └── templates/            # Templates HTML
│       ├── base.html         # Template base
│       ├── dashboard/        # Templates específicos
│       │   ├── dashboard.html
│       │   ├── surveys_list.html
│       │   └── responses_list.html
└── manage.py                 # Script de gerenciamento Django
```

### FastAPI Collector (`collector/`)
```
collector/
├── api/                      # Endpoints da API
│   └── nps.py               # Endpoints NPS
├── schemas/                  # Schemas Pydantic e Modelos SQLAlchemy
│   ├── models.py            # Modelos SQLAlchemy
│   └── schemas.py           # Schemas Pydantic
├── crud/                     # Operações CRUD
│   └── crud.py              # Funções de banco de dados
├── main.py                   # Aplicação FastAPI principal
└── database.py               # Configuração do banco
```

## 🗄️ Modelos de Dados

### Django Models (`dashboard/dashboard/models.py`)

#### Customer
```python
class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    company = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Survey
```python
class Survey(models.Model):
    SURVEY_TYPES = [
        ('nps', 'NPS (Net Promoter Score)'),
        ('csat', 'CSAT (Customer Satisfaction)'),
        ('ces', 'CES (Customer Effort Score)'),
        ('custom', 'Personalizada'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    survey_type = models.CharField(max_length=10, choices=SURVEY_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

#### Response
```python
class Response(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
```

### SQLAlchemy Models (`collector/schemas/models.py`)

Os modelos SQLAlchemy são idênticos aos Django, mas usando a sintaxe do SQLAlchemy:

```python
class Customer(Base):
    __tablename__ = "dashboard_customer"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(Email, nullable=False)
    company = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

## 🔌 Endpoints da API

### FastAPI Collector

#### POST `/api/nps/submit`
**Função**: `submit_nps_response()` em `collector/api/nps.py`

**Fluxo**:
1. Valida se a pesquisa existe e está ativa
2. Valida o score NPS (0-10)
3. Busca ou cria o cliente
4. Verifica se já existe resposta para o cliente
5. Cria a resposta no banco
6. Retorna confirmação

**Validações**:
- Score entre 0 e 10
- Pesquisa ativa e tipo NPS
- Email válido
- Não permite respostas duplicadas

#### GET `/api/nps/results`
**Função**: `get_nps_results()` em `collector/api/nps.py`

**Funcionalidades**:
- Lista respostas com paginação
- Filtro por pesquisa específica
- Ordenação por data de envio

#### GET `/api/nps/summary`
**Função**: `get_nps_summary()` em `collector/api/nps.py`

**Cálculos**:
- Total de respostas
- Score NPS médio
- Percentual de promotores, neutros e detratores
- Estatísticas por pesquisa

### Django Dashboard

#### GET `/`
**Função**: `dashboard()` em `dashboard/dashboard/views.py`

**Funcionalidades**:
- Estatísticas gerais
- Gráfico de distribuição NPS
- Gráfico de tendência temporal
- Cálculo de score NPS

#### GET `/responses/`
**Função**: `responses_list()` em `dashboard/dashboard/views.py`

**Filtros**:
- Por pesquisa
- Por cliente
- Por período (data inicial/final)

## 🎨 Frontend (Templates)

### Template Base (`base.html`)
- Bootstrap 5.3.0
- Chart.js para gráficos
- Font Awesome para ícones
- Sidebar responsiva
- Sistema de alertas

### Dashboard (`dashboard.html`)
- Cards com estatísticas
- Gráfico de distribuição NPS (Chart.js)
- Gráfico de tendência temporal
- Ações rápidas

### Lista de Respostas (`responses_list.html`)
- Tabela responsiva
- Filtros avançados
- Paginação
- Exportação de dados

## 🗃️ Operações de Banco de Dados

### CRUD Operations (`collector/crud/crud.py`)

#### Clientes
```python
def get_customer_by_email(db: Session, email: str) -> Optional[Customer]
def create_customer(db: Session, customer: CustomerCreate) -> Customer
```

#### Pesquisas
```python
def get_survey(db: Session, survey_id: int) -> Optional[Survey]
def get_active_surveys(db: Session) -> List[Survey]
```

#### Respostas
```python
def create_response(db: Session, response: ResponseCreate, customer_id: int) -> Response
def get_responses_by_survey(db: Session, survey_id: int) -> List[Response]
def get_nps_responses(db: Session) -> List[Response]
```

#### Cálculos NPS
```python
def calculate_nps_score(responses: List[Response]) -> dict
```

## 🔧 Configuração de Desenvolvimento

### 1. Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Dependências
```bash
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
```bash
cp env.example .env
# Configure DB_HOST, DB_USER, DB_PASSWORD, etc.
```

### 4. Banco de Dados
```bash
# Execute o script de inicialização
sqlcmd -S localhost -i database/init.sql

# Migrações Django
cd dashboard
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Executar Aplicações
```bash
# Terminal 1 - Django
cd dashboard
python manage.py runserver

# Terminal 2 - FastAPI
cd collector
uvicorn main:app --reload --port 8001
```

## 🧪 Testes

### Testes Django
```bash
cd dashboard
python manage.py test
```

### Testes FastAPI
```bash
cd collector
pytest
```

### Testes de Integração
```bash
# Teste de conexão com banco
python scripts/test_db_connection.py
```

## 📊 Cálculos NPS

### Fórmula NPS
```
NPS = ((Promotores - Detratores) / Total de Respostas) × 100
```

### Categorização
- **Promotores**: Score 9-10
- **Neutros**: Score 7-8
- **Detratores**: Score 0-6

### Implementação
```python
def calculate_nps_score(responses: List[Response]) -> dict:
    promoters = sum(1 for r in responses if r.score and r.score >= 9)
    passives = sum(1 for r in responses if r.score and r.score in [7, 8])
    detractors = sum(1 for r in responses if r.score and r.score <= 6)
    
    total = len(responses)
    nps_score = ((promoters - detractors) / total * 100) if total > 0 else 0
    
    return {
        'total_responses': total,
        'promoters': promoters,
        'passives': passives,
        'detractors': detractors,
        'nps_score': round(nps_score, 2)
    }
```

## 🚀 Deploy

### Docker
```bash
# Usar docker-compose.yml
docker-compose up -d
```

### Produção
1. Configure variáveis de ambiente
2. Use servidor web (Nginx + Gunicorn)
3. Configure HTTPS
4. Configure backup do banco
5. Configure monitoramento

## 🔍 Debugging

### Logs Django
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Logs FastAPI
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Info message")
```

### Debug SQL
```python
# Django
from django.db import connection
print(connection.queries)

# SQLAlchemy
engine.echo = True
```

## 📈 Performance

### Otimizações Django
- Use `select_related()` e `prefetch_related()`
- Implemente cache para consultas frequentes
- Use paginação para listas grandes

### Otimizações FastAPI
- Use async/await quando possível
- Implemente cache Redis
- Use connection pooling

### Otimizações Banco
- Crie índices apropriados
- Use views materializadas para relatórios
- Configure backup automático

## 🔒 Segurança

### Validação de Dados
- Pydantic para FastAPI
- Django Forms para Django
- Validação de email
- Sanitização de inputs

### CORS
```python
# Configurado em settings.py e main.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Rate Limiting
```python
# Implementar com slowapi
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

## 📝 Contribuição

### Padrões de Código
- Use Black para formatação
- Use Flake8 para linting
- Documente funções complexas
- Use type hints

### Git Workflow
1. Crie uma branch para sua feature
2. Faça commits pequenos e descritivos
3. Teste suas mudanças
4. Abra um Pull Request

### Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: formatação de código
refactor: refatoração
test: adiciona testes
```

---

*Este guia deve ser atualizado conforme o projeto evolui.*
