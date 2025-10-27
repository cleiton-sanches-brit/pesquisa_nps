# 📚 Documentação da API - Survey Analytics

## 🌐 Visão Geral

O Survey Analytics possui duas APIs principais:

- **FastAPI Collector** (Porta 8001): Coleta de respostas de pesquisas
- **Django Dashboard** (Porta 8000): Painel administrativo e relatórios

## 🚀 FastAPI Collector API

### Base URL
```
http://localhost:8001
```

### Autenticação
Atualmente não requer autenticação para endpoints públicos de coleta.

### Endpoints Disponíveis

#### 1. **POST** `/api/nps/submit`
Envia uma resposta de pesquisa NPS.

**Request Body:**
```json
{
  "customer_name": "string",
  "customer_email": "string",
  "customer_company": "string (opcional)",
  "survey_id": "integer",
  "score": "integer (0-10)",
  "comment": "string (opcional)"
}
```

**Exemplo de Request:**
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

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Resposta enviada com sucesso",
  "response_id": 123
}
```

**Possíveis Erros:**
- `400 Bad Request`: Score inválido, pesquisa inativa, ou resposta duplicada
- `404 Not Found`: Pesquisa não encontrada

---

#### 2. **GET** `/api/nps/results`
Lista resultados de pesquisas NPS.

**Query Parameters:**
- `survey_id` (opcional): ID da pesquisa específica
- `skip` (opcional): Número de registros para pular (padrão: 0)
- `limit` (opcional): Número máximo de registros (padrão: 100)

**Exemplo de Request:**
```bash
curl -X GET "http://localhost:8001/api/nps/results?survey_id=1&limit=50"
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "customer_name": "João Silva",
    "customer_email": "joao@example.com",
    "customer_company": "Empresa ABC",
    "survey_id": 1,
    "score": 9,
    "comment": "Excelente atendimento!",
    "submitted_at": "2024-01-15T10:30:00Z"
  }
]
```

---

#### 3. **GET** `/api/nps/summary`
Retorna resumo agregado de todas as pesquisas NPS.

**Exemplo de Request:**
```bash
curl -X GET "http://localhost:8001/api/nps/summary"
```

**Response (200 OK):**
```json
{
  "total_responses": 150,
  "average_nps": 45.2,
  "promoters_percentage": 60.0,
  "passives_percentage": 25.0,
  "detractors_percentage": 15.0,
  "surveys": [
    {
      "survey_id": 1,
      "survey_title": "Pesquisa de Satisfação",
      "total_responses": 100,
      "average_score": 8.5,
      "promoters": 60,
      "passives": 25,
      "detractors": 15,
      "nps_score": 45.0
    }
  ]
}
```

---

### Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Erro de validação |
| 500 | Internal Server Error |

---

## 🎛️ Django Dashboard API

### Base URL
```
http://localhost:8000
```

### Autenticação
Requer login de usuário administrador.

### Endpoints Disponíveis

#### 1. **GET** `/`
Dashboard principal com gráficos e estatísticas.

**Response:** Página HTML com dashboard interativo

---

#### 2. **GET** `/surveys/`
Lista todas as pesquisas cadastradas.

**Response:** Página HTML com lista de pesquisas

---

#### 3. **GET** `/responses/`
Lista todas as respostas com filtros.

**Query Parameters:**
- `survey`: ID da pesquisa
- `customer`: ID do cliente
- `date_from`: Data inicial (YYYY-MM-DD)
- `date_to`: Data final (YYYY-MM-DD)

**Exemplo:**
```
http://localhost:8000/responses/?survey=1&date_from=2024-01-01&date_to=2024-01-31
```

---

#### 4. **GET** `/export/csv/`
Exporta todas as respostas em formato CSV.

**Response:** Arquivo CSV para download

---

#### 5. **GET** `/export/excel/`
Exporta todas as respostas em formato Excel.

**Response:** Arquivo Excel (.xlsx) para download

---

#### 6. **GET** `/admin/`
Interface administrativa do Django.

**Funcionalidades:**
- Gerenciar clientes
- Gerenciar pesquisas
- Gerenciar respostas
- Visualizar relatórios

---

#### 7. **GET** `/api/nps-data/`
API interna para dados NPS (usado pelos gráficos).

**Response (JSON):**
```json
{
  "distribution": [
    {"score": 0, "count": 5},
    {"score": 1, "count": 3},
    {"score": 9, "count": 25},
    {"score": 10, "count": 30}
  ],
  "categories": {
    "promoters": 55,
    "passives": 25,
    "detractors": 20
  },
  "trend": [
    {
      "date": "2024-01-15",
      "nps": 45.2,
      "responses": 12
    }
  ]
}
```

---

## 📊 Modelos de Dados

### Customer (Cliente)
```json
{
  "id": "integer",
  "name": "string",
  "email": "string (email válido)",
  "company": "string (opcional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Survey (Pesquisa)
```json
{
  "id": "integer",
  "title": "string",
  "description": "string (opcional)",
  "survey_type": "string (nps|csat|ces|custom)",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Response (Resposta)
```json
{
  "id": "integer",
  "customer_id": "integer",
  "survey_id": "integer",
  "score": "integer (0-10, opcional)",
  "comment": "string (opcional)",
  "submitted_at": "datetime",
  "ip_address": "string",
  "user_agent": "string"
}
```

---

## 🔧 Configuração e Uso

### 1. Instalação
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd survey_analytics

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração do Banco
```bash
# Configure o arquivo .env
cp env.example .env
# Edite o arquivo .env com suas credenciais do SQL Server

# Execute as migrações
cd dashboard
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Executar as APIs
```bash
# Terminal 1 - Django Dashboard
cd dashboard
python manage.py runserver

# Terminal 2 - FastAPI Collector
cd collector
uvicorn main:app --reload --port 8001
```

### 4. Acessar Documentação Interativa
- **FastAPI Swagger**: http://localhost:8001/docs
- **FastAPI ReDoc**: http://localhost:8001/redoc
- **Django Admin**: http://localhost:8000/admin/

---

## 🧪 Exemplos de Uso

### Enviar Resposta NPS
```python
import requests

url = "http://localhost:8001/api/nps/submit"
data = {
    "customer_name": "Maria Santos",
    "customer_email": "maria@empresa.com",
    "customer_company": "Tech Corp",
    "survey_id": 1,
    "score": 8,
    "comment": "Bom atendimento, mas pode melhorar"
}

response = requests.post(url, json=data)
print(response.json())
```

### Obter Resumo NPS
```python
import requests

url = "http://localhost:8001/api/nps/summary"
response = requests.get(url)
data = response.json()

print(f"Total de respostas: {data['total_responses']}")
print(f"NPS Score médio: {data['average_nps']}")
print(f"Promotores: {data['promoters_percentage']}%")
```

### Exportar Dados
```python
import requests

# Exportar CSV
csv_response = requests.get("http://localhost:8000/export/csv/")
with open("respostas.csv", "wb") as f:
    f.write(csv_response.content)

# Exportar Excel
excel_response = requests.get("http://localhost:8000/export/excel/")
with open("respostas.xlsx", "wb") as f:
    f.write(excel_response.content)
```

---

## 🚨 Tratamento de Erros

### Erros Comuns

#### 1. **Pesquisa Não Encontrada**
```json
{
  "detail": "Pesquisa não encontrada"
}
```

#### 2. **Score Inválido**
```json
{
  "detail": "Score deve estar entre 0 e 10"
}
```

#### 3. **Resposta Duplicada**
```json
{
  "detail": "Já existe uma resposta para este cliente nesta pesquisa"
}
```

#### 4. **Pesquisa Inativa**
```json
{
  "detail": "Pesquisa não está ativa"
}
```

---

## 📈 Monitoramento e Logs

### Health Check
```bash
# Verificar status da API
curl http://localhost:8001/health
curl http://localhost:8000/health
```

### Logs
- **Django**: Logs no console durante desenvolvimento
- **FastAPI**: Logs no console com nível DEBUG
- **Produção**: Configure logging apropriado

---

## 🔒 Segurança

### Recomendações
1. **Rate Limiting**: Implemente limitação de taxa para endpoints públicos
2. **Validação**: Todos os inputs são validados com Pydantic
3. **CORS**: Configurado para desenvolvimento, ajuste para produção
4. **HTTPS**: Use HTTPS em produção
5. **Autenticação**: Implemente autenticação JWT se necessário

---

## 📞 Suporte

Para dúvidas ou problemas:
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/survey_analytics/issues)
- **Documentação**: Consulte este arquivo e o README.md
- **API Docs**: Use a documentação interativa do FastAPI

---

*Última atualização: Janeiro 2024*
