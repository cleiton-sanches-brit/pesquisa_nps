# 🎛️ Guia do Django Dashboard - Survey Analytics

## 📋 Visão Geral

O Django Dashboard é a interface administrativa do Survey Analytics, fornecendo:

- **Dashboard interativo** com gráficos e estatísticas
- **Gerenciamento de pesquisas** e respostas
- **Relatórios e exportação** de dados
- **Interface administrativa** completa
- **Filtros avançados** para análise de dados

## 🌐 URLs e Rotas

### URLs Principais
```
http://localhost:8000/
├── /                    # Dashboard principal
├── /surveys/           # Lista de pesquisas
├── /responses/         # Lista de respostas
├── /export/csv/        # Exportar CSV
├── /export/excel/      # Exportar Excel
├── /admin/             # Interface administrativa
└── /api/nps-data/      # API interna para gráficos
```

## 🏠 Dashboard Principal (`/`)

### Funcionalidades
- **Estatísticas gerais**: Total de pesquisas, respostas, clientes
- **Score NPS**: Cálculo e exibição do NPS atual
- **Gráfico de distribuição**: Notas NPS de 0-10
- **Gráfico de tendência**: Evolução do NPS ao longo do tempo
- **Ações rápidas**: Links para funcionalidades principais

### Dados Exibidos
```python
# Estatísticas gerais
total_surveys = Survey.objects.count()
total_responses = Response.objects.count()
total_customers = Customer.objects.count()
recent_responses = Response.objects.filter(
    submitted_at__gte=thirty_days_ago
).count()

# Cálculo NPS
promoters = Response.objects.filter(score__gte=9, survey__survey_type='nps').count()
passives = Response.objects.filter(score__in=[7,8], survey__survey_type='nps').count()
detractors = Response.objects.filter(score__lte=6, survey__survey_type='nps').count()
nps_score = ((promoters - detractors) / total_responses) * 100
```

### Gráficos (Chart.js)
1. **Distribuição NPS**: Gráfico de barras com cores por categoria
2. **Tendência Temporal**: Gráfico de linha com evolução do NPS

## 📊 Lista de Pesquisas (`/surveys/`)

### Funcionalidades
- **Cards visuais** para cada pesquisa
- **Informações resumidas**: Tipo, perguntas, respostas
- **Status visual**: Ativa/Inativa com badges
- **Ações rápidas**: Editar, ver respostas
- **Criação de pesquisas**: Link para admin

### Template: `surveys_list.html`
```html
<!-- Card de pesquisa -->
<div class="card h-100">
    <div class="card-header">
        <h6>{{ survey.title }}</h6>
        <span class="badge bg-success">Ativa</span>
    </div>
    <div class="card-body">
        <p>{{ survey.description|truncatechars:100 }}</p>
        <div class="row text-center">
            <div class="col-4">
                <strong>{{ survey.get_survey_type_display }}</strong>
            </div>
            <div class="col-4">
                <strong>{{ survey.questions.count }}</strong>
            </div>
            <div class="col-4">
                <strong>{{ survey.responses.count }}</strong>
            </div>
        </div>
    </div>
</div>
```

## 📝 Lista de Respostas (`/responses/`)

### Funcionalidades
- **Tabela responsiva** com todas as respostas
- **Filtros avançados**: Por pesquisa, cliente, data
- **Informações detalhadas**: Cliente, pesquisa, nota, comentário
- **Categorização NPS**: Cores por categoria (Promotor/Neutro/Detrator)
- **Exportação**: Links para CSV e Excel

### Filtros Disponíveis
```python
# Filtros implementados
survey_id = request.GET.get('survey')
customer_id = request.GET.get('customer')
date_from = request.GET.get('date_from')
date_to = request.GET.get('date_to')

# Aplicação dos filtros
if survey_id:
    responses = responses.filter(survey_id=survey_id)
if customer_id:
    responses = responses.filter(customer_id=customer_id)
if date_from:
    responses = responses.filter(submitted_at__date__gte=date_from)
if date_to:
    responses = responses.filter(submitted_at__date__lte=date_to)
```

### Template: `responses_list.html`
```html
<!-- Filtros -->
<form method="get" class="row g-3">
    <div class="col-md-3">
        <select class="form-select" name="survey">
            <option value="">Todas as pesquisas</option>
            {% for survey in surveys %}
            <option value="{{ survey.id }}">{{ survey.title }}</option>
            {% endfor %}
        </select>
    </div>
    <!-- Mais filtros... -->
</form>

<!-- Tabela de respostas -->
<table class="table table-hover">
    <thead>
        <tr>
            <th>Cliente</th>
            <th>Pesquisa</th>
            <th>Nota</th>
            <th>Comentário</th>
            <th>Data</th>
        </tr>
    </thead>
    <tbody>
        {% for response in responses %}
        <tr>
            <td>{{ response.customer.name }}</td>
            <td>{{ response.survey.title }}</td>
            <td>
                <span class="badge bg-success">{{ response.score }}</span>
            </td>
            <td>{{ response.comment|truncatechars:50 }}</td>
            <td>{{ response.submitted_at|date:"d/m/Y H:i" }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## 📤 Exportação de Dados

### Exportar CSV (`/export/csv/`)
```python
def export_responses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="respostas.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Email', 'Empresa', 'Pesquisa', 'Tipo', 'Nota', 'Comentário', 'Data'])
    
    responses = Response.objects.select_related('customer', 'survey').all()
    for resp in responses:
        writer.writerow([
            resp.customer.name,
            resp.customer.email,
            resp.customer.company,
            resp.survey.title,
            resp.survey.get_survey_type_display(),
            resp.score or '',
            resp.comment,
            resp.submitted_at.strftime('%d/%m/%Y %H:%M')
        ])
    
    return response
```

### Exportar Excel (`/export/excel/`)
```python
def export_responses_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="respostas.xlsx"'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Respostas"
    
    # Cabeçalhos
    headers = ['Cliente', 'Email', 'Empresa', 'Pesquisa', 'Tipo', 'Nota', 'Comentário', 'Data']
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)
    
    # Dados
    responses = Response.objects.select_related('customer', 'survey').all()
    for row, resp in enumerate(responses, 2):
        ws.cell(row=row, column=1, value=resp.customer.name)
        ws.cell(row=row, column=2, value=resp.customer.email)
        # ... mais colunas
    
    wb.save(response)
    return response
```

## 🔧 Interface Administrativa (`/admin/`)

### Modelos Administráveis

#### Customer Admin
```python
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'created_at', 'response_count']
    list_filter = ['created_at', 'company']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']
```

#### Survey Admin
```python
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'survey_type', 'is_active', 'created_by', 'created_at', 'response_count']
    list_filter = ['survey_type', 'is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
```

#### Response Admin
```python
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['customer', 'survey', 'score', 'nps_category_display', 'submitted_at']
    list_filter = ['survey__survey_type', 'submitted_at', 'score']
    search_fields = ['customer__name', 'customer__email', 'survey__title']
    readonly_fields = ['submitted_at', 'ip_address', 'user_agent']
```

### Funcionalidades do Admin
- **Filtros avançados** por data, tipo, status
- **Busca** em campos relevantes
- **Ordenação** por qualquer campo
- **Ações em lote** para múltiplos registros
- **Visualização detalhada** de cada registro

## 🎨 Frontend e Templates

### Template Base (`base.html`)
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Sidebar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sidebar">
        <!-- Navegação -->
    </nav>
    
    <!-- Main Content -->
    <div class="main-content">
        <!-- Conteúdo da página -->
        {% block content %}{% endblock %}
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Estilos CSS Customizados
```css
.sidebar {
    min-height: 100vh;
    background-color: #f8f9fa;
}

.main-content {
    margin-left: 0;
}

@media (min-width: 768px) {
    .main-content {
        margin-left: 250px;
    }
}

.card-stat {
    border-left: 4px solid #007bff;
}

.card-stat.success {
    border-left-color: #28a745;
}

.card-stat.warning {
    border-left-color: #ffc107;
}

.card-stat.danger {
    border-left-color: #dc3545;
}
```

## 📊 Gráficos e Visualizações

### Gráfico de Distribuição NPS
```javascript
const npsDistribution = {{ nps_distribution|safe }};

const ctx1 = document.getElementById('npsDistributionChart').getContext('2d');
const distributionChart = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: npsDistribution.map(item => item.score),
        datasets: [{
            label: 'Quantidade de Respostas',
            data: npsDistribution.map(item => item.count),
            backgroundColor: npsDistribution.map(item => {
                const score = item.score;
                if (score >= 9) return '#28a745';
                if (score >= 7) return '#ffc107';
                return '#dc3545';
            })
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true },
            x: { title: { display: true, text: 'Nota NPS' } }
        }
    }
});
```

### Gráfico de Tendência Temporal
```javascript
const trendData = {{ trend_data|safe }};

const ctx2 = document.getElementById('trendChart').getContext('2d');
const trendChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: trendData.map(item => {
            const date = new Date(item.date);
            return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
        }),
        datasets: [{
            label: 'NPS Score',
            data: trendData.map(item => item.nps),
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            tension: 0.4,
            fill: true
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true },
            x: { title: { display: true, text: 'Data' } }
        }
    }
});
```

## 🔌 API Interna (`/api/nps-data/`)

### Endpoint para Dados dos Gráficos
```python
def api_nps_data(request):
    # Distribuição de notas NPS
    distribution = Response.objects.filter(
        score__isnull=False,
        survey__survey_type='nps'
    ).values('score').annotate(count=Count('score')).order_by('score')
    
    # Categorias NPS
    promoters = Response.objects.filter(score__gte=9, survey__survey_type='nps').count()
    passives = Response.objects.filter(score__in=[7,8], survey__survey_type='nps').count()
    detractors = Response.objects.filter(score__lte=6, survey__survey_type='nps').count()
    
    # Tendência temporal
    trend_data = []
    for i in range(30):  # Últimos 30 dias
        date = timezone.now() - timedelta(days=i)
        day_responses = Response.objects.filter(
            submitted_at__date=date.date(),
            survey__survey_type='nps'
        )
        # ... cálculos
    
    data = {
        'distribution': list(distribution),
        'categories': {
            'promoters': promoters,
            'passives': passives,
            'detractors': detractors
        },
        'trend': trend_data
    }
    
    return JsonResponse(data)
```

## 🚀 Deploy e Configuração

### Configurações de Produção
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# Configurações de banco para produção
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# Configurações de arquivos estáticos
STATIC_ROOT = '/var/www/survey_analytics/static/'
MEDIA_ROOT = '/var/www/survey_analytics/media/'
```

### Comandos de Deploy
```bash
# Coletar arquivos estáticos
python manage.py collectstatic

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar com Gunicorn
gunicorn survey_analytics.wsgi:application --bind 0.0.0.0:8000
```

## 🔍 Monitoramento e Logs

### Configuração de Logs
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'dashboard': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Métricas Importantes
- **Tempo de resposta** das páginas
- **Número de respostas** por dia
- **Score NPS** médio
- **Uso de filtros** na interface
- **Downloads** de exportação

---

*Este guia cobre todas as funcionalidades do Django Dashboard do Survey Analytics.*
