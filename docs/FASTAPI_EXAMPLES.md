# 🚀 Exemplos Práticos - FastAPI Collector

## 📋 Índice
- [Configuração Inicial](#configuração-inicial)
- [Enviando Respostas NPS](#enviando-respostas-nps)
- [Consultando Resultados](#consultando-resultados)
- [Obtendo Resumos](#obtendo-resumos)
- [Tratamento de Erros](#tratamento-de-erros)
- [Exemplos em Python](#exemplos-em-python)
- [Exemplos em JavaScript](#exemplos-em-javascript)
- [Exemplos em cURL](#exemplos-em-curl)

## 🔧 Configuração Inicial

### 1. Iniciar o Servidor
```bash
cd collector
uvicorn main:app --reload --port 8001
```

### 2. Verificar Status
```bash
curl http://localhost:8001/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### 3. Acessar Documentação Interativa
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

## 📝 Enviando Respostas NPS

### Exemplo Básico
```python
import requests

url = "http://localhost:8001/api/nps/submit"
data = {
    "customer_name": "João Silva",
    "customer_email": "joao@empresa.com",
    "customer_company": "Tech Corp",
    "survey_id": 1,
    "score": 9,
    "comment": "Excelente atendimento!"
}

response = requests.post(url, json=data)
print(response.json())
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "message": "Resposta enviada com sucesso",
  "response_id": 123
}
```

### Exemplo com Validação de Erro
```python
import requests

url = "http://localhost:8001/api/nps/submit"
data = {
    "customer_name": "Maria Santos",
    "customer_email": "maria@empresa.com",
    "survey_id": 1,
    "score": 15,  # Score inválido (deve ser 0-10)
    "comment": "Muito bom!"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}")
```

**Resposta de Erro:**
```json
{
  "detail": "Score deve estar entre 0 e 10"
}
```

### Exemplo com Resposta Duplicada
```python
import requests

url = "http://localhost:8001/api/nps/submit"
data = {
    "customer_name": "Pedro Costa",
    "customer_email": "pedro@empresa.com",
    "survey_id": 1,
    "score": 8,
    "comment": "Bom atendimento"
}

# Primeira tentativa
response1 = requests.post(url, json=data)
print(f"Primeira tentativa: {response1.json()}")

# Segunda tentativa (mesmo cliente, mesma pesquisa)
response2 = requests.post(url, json=data)
print(f"Segunda tentativa: {response2.json()}")
```

**Respostas:**
```json
// Primeira tentativa
{
  "success": true,
  "message": "Resposta enviada com sucesso",
  "response_id": 124
}

// Segunda tentativa
{
  "detail": "Já existe uma resposta para este cliente nesta pesquisa"
}
```

---

## 📊 Consultando Resultados

### Listar Todas as Respostas
```python
import requests

url = "http://localhost:8001/api/nps/results"
response = requests.get(url)
data = response.json()

print(f"Total de respostas: {len(data)}")
for resp in data:
    print(f"Cliente: {resp['customer_name']} - Score: {resp['score']}")
```

### Filtrar por Pesquisa
```python
import requests

url = "http://localhost:8001/api/nps/results"
params = {"survey_id": 1}
response = requests.get(url, params=params)
data = response.json()

print(f"Respostas da pesquisa 1: {len(data)}")
```

### Paginação
```python
import requests

url = "http://localhost:8001/api/nps/results"
params = {"skip": 0, "limit": 10}
response = requests.get(url, params=params)
data = response.json()

print(f"Primeiras 10 respostas: {len(data)}")
```

---

## 📈 Obtendo Resumos

### Resumo Completo
```python
import requests

url = "http://localhost:8001/api/nps/summary"
response = requests.get(url)
data = response.json()

print("=== RESUMO NPS ===")
print(f"Total de respostas: {data['total_responses']}")
print(f"NPS Score médio: {data['average_nps']}")
print(f"Promotores: {data['promoters_percentage']}%")
print(f"Neutros: {data['passives_percentage']}%")
print(f"Detratores: {data['detractors_percentage']}%")

print("\n=== POR PESQUISA ===")
for survey in data['surveys']:
    print(f"Pesquisa: {survey['survey_title']}")
    print(f"  Respostas: {survey['total_responses']}")
    print(f"  NPS Score: {survey['nps_score']}")
    print(f"  Promotores: {survey['promoters']}")
    print(f"  Neutros: {survey['passives']}")
    print(f"  Detratores: {survey['detractors']}")
    print()
```

### Análise de Tendências
```python
import requests
from datetime import datetime, timedelta

url = "http://localhost:8001/api/nps/summary"
response = requests.get(url)
data = response.json()

# Calcular tendência
if data['total_responses'] > 0:
    if data['average_nps'] > 0:
        status = "Positivo"
    elif data['average_nps'] == 0:
        status = "Neutro"
    else:
        status = "Negativo"
    
    print(f"Status NPS: {status}")
    print(f"Score: {data['average_nps']}")
```

---

## ⚠️ Tratamento de Erros

### Classe para Tratamento de Erros
```python
import requests
from typing import Dict, Any

class NPSError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def submit_nps_response(data: Dict[str, Any]) -> Dict[str, Any]:
    url = "http://localhost:8001/api/nps/submit"
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error_data = response.json()
            raise NPSError(f"Erro de validação: {error_data['detail']}", 400)
        elif response.status_code == 404:
            raise NPSError("Pesquisa não encontrada", 404)
        else:
            raise NPSError(f"Erro inesperado: {response.status_code}", response.status_code)
            
    except requests.exceptions.ConnectionError:
        raise NPSError("Não foi possível conectar à API", 0)
    except requests.exceptions.Timeout:
        raise NPSError("Timeout na requisição", 0)

# Exemplo de uso
try:
    data = {
        "customer_name": "Teste",
        "customer_email": "teste@empresa.com",
        "survey_id": 1,
        "score": 9,
        "comment": "Teste"
    }
    
    result = submit_nps_response(data)
    print(f"Sucesso: {result['message']}")
    
except NPSError as e:
    print(f"Erro NPS: {e.message} (Status: {e.status_code})")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

---

## 🐍 Exemplos em Python

### Cliente Python Completo
```python
import requests
import json
from typing import Dict, List, Optional

class SurveyAnalyticsClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def submit_response(self, customer_name: str, customer_email: str, 
                       survey_id: int, score: int, comment: str = None, 
                       company: str = None) -> Dict:
        """Envia uma resposta NPS"""
        url = f"{self.base_url}/api/nps/submit"
        data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_company": company,
            "survey_id": survey_id,
            "score": score,
            "comment": comment
        }
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_results(self, survey_id: Optional[int] = None, 
                   skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtém resultados de pesquisas"""
        url = f"{self.base_url}/api/nps/results"
        params = {"skip": skip, "limit": limit}
        
        if survey_id:
            params["survey_id"] = survey_id
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_summary(self) -> Dict:
        """Obtém resumo agregado"""
        url = f"{self.base_url}/api/nps/summary"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict:
        """Verifica status da API"""
        url = f"{self.base_url}/health"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# Exemplo de uso
if __name__ == "__main__":
    client = SurveyAnalyticsClient()
    
    # Verificar saúde da API
    health = client.health_check()
    print(f"API Status: {health['status']}")
    
    # Enviar resposta
    result = client.submit_response(
        customer_name="João Silva",
        customer_email="joao@empresa.com",
        survey_id=1,
        score=9,
        comment="Excelente!",
        company="Tech Corp"
    )
    print(f"Resposta enviada: {result['message']}")
    
    # Obter resumo
    summary = client.get_summary()
    print(f"NPS Score: {summary['average_nps']}")
```

---

## 🌐 Exemplos em JavaScript

### Cliente JavaScript (Node.js)
```javascript
const axios = require('axios');

class SurveyAnalyticsClient {
    constructor(baseUrl = 'http://localhost:8001') {
        this.baseUrl = baseUrl;
        this.client = axios.create({
            baseURL: baseUrl,
            timeout: 5000
        });
    }
    
    async submitResponse(customerName, customerEmail, surveyId, score, comment = null, company = null) {
        try {
            const response = await this.client.post('/api/nps/submit', {
                customer_name: customerName,
                customer_email: customerEmail,
                customer_company: company,
                survey_id: surveyId,
                score: score,
                comment: comment
            });
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao enviar resposta: ${error.response?.data?.detail || error.message}`);
        }
    }
    
    async getResults(surveyId = null, skip = 0, limit = 100) {
        try {
            const params = { skip, limit };
            if (surveyId) params.survey_id = surveyId;
            
            const response = await this.client.get('/api/nps/results', { params });
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter resultados: ${error.response?.data?.detail || error.message}`);
        }
    }
    
    async getSummary() {
        try {
            const response = await this.client.get('/api/nps/summary');
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter resumo: ${error.response?.data?.detail || error.message}`);
        }
    }
    
    async healthCheck() {
        try {
            const response = await this.client.get('/health');
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao verificar saúde da API: ${error.message}`);
        }
    }
}

// Exemplo de uso
async function exemplo() {
    const client = new SurveyAnalyticsClient();
    
    try {
        // Verificar saúde
        const health = await client.healthCheck();
        console.log('API Status:', health.status);
        
        // Enviar resposta
        const result = await client.submitResponse(
            'João Silva',
            'joao@empresa.com',
            1,
            9,
            'Excelente!',
            'Tech Corp'
        );
        console.log('Resposta enviada:', result.message);
        
        // Obter resumo
        const summary = await client.getSummary();
        console.log('NPS Score:', summary.average_nps);
        
    } catch (error) {
        console.error('Erro:', error.message);
    }
}

exemplo();
```

### Cliente JavaScript (Browser)
```javascript
class SurveyAnalyticsClient {
    constructor(baseUrl = 'http://localhost:8001') {
        this.baseUrl = baseUrl;
    }
    
    async submitResponse(customerName, customerEmail, surveyId, score, comment = null, company = null) {
        const response = await fetch(`${this.baseUrl}/api/nps/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_name: customerName,
                customer_email: customerEmail,
                customer_company: company,
                survey_id: surveyId,
                score: score,
                comment: comment
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Erro: ${error.detail}`);
        }
        
        return await response.json();
    }
    
    async getResults(surveyId = null, skip = 0, limit = 100) {
        let url = `${this.baseUrl}/api/nps/results?skip=${skip}&limit=${limit}`;
        if (surveyId) url += `&survey_id=${surveyId}`;
        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Erro ao obter resultados');
        }
        
        return await response.json();
    }
    
    async getSummary() {
        const response = await fetch(`${this.baseUrl}/api/nps/summary`);
        if (!response.ok) {
            throw new Error('Erro ao obter resumo');
        }
        
        return await response.json();
    }
}

// Exemplo de uso no browser
const client = new SurveyAnalyticsClient();

// Enviar resposta via formulário
document.getElementById('npsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const result = await client.submitResponse(
            formData.get('customer_name'),
            formData.get('customer_email'),
            parseInt(formData.get('survey_id')),
            parseInt(formData.get('score')),
            formData.get('comment'),
            formData.get('company')
        );
        
        alert(`Resposta enviada: ${result.message}`);
        e.target.reset();
        
    } catch (error) {
        alert(`Erro: ${error.message}`);
    }
});
```

---

## 💻 Exemplos em cURL

### Enviar Resposta
```bash
curl -X POST "http://localhost:8001/api/nps/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "João Silva",
    "customer_email": "joao@empresa.com",
    "customer_company": "Tech Corp",
    "survey_id": 1,
    "score": 9,
    "comment": "Excelente atendimento!"
  }'
```

### Obter Resultados
```bash
# Todas as respostas
curl -X GET "http://localhost:8001/api/nps/results"

# Respostas de uma pesquisa específica
curl -X GET "http://localhost:8001/api/nps/results?survey_id=1"

# Com paginação
curl -X GET "http://localhost:8001/api/nps/results?skip=0&limit=10"
```

### Obter Resumo
```bash
curl -X GET "http://localhost:8001/api/nps/summary"
```

### Verificar Status
```bash
curl -X GET "http://localhost:8001/health"
```

---

## 🔧 Configuração Avançada

### Timeout e Retry
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Uso
session = create_session_with_retries()
response = session.post("http://localhost:8001/api/nps/submit", json=data)
```

### Logging
```python
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def submit_with_logging(data):
    logger.info(f"Enviando resposta: {data['customer_name']}")
    
    try:
        response = requests.post("http://localhost:8001/api/nps/submit", json=data)
        response.raise_for_status()
        
        logger.info(f"Resposta enviada com sucesso: {response.json()}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        raise
```

---

*Esta documentação fornece exemplos práticos para integração com a API FastAPI Collector.*
