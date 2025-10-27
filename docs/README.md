# 📚 Documentação - Survey Analytics

Bem-vindo à documentação completa do Survey Analytics! Este sistema híbrido combina Django para administração e FastAPI para coleta de respostas de pesquisas NPS, CSAT e CES.

## 📖 Índice da Documentação

### 🚀 Guias de Início Rápido
- **[Guia de Instalação](INSTALLATION_GUIDE.md)** - Instalação completa passo a passo
- **[API Documentation](API_DOCUMENTATION.md)** - Documentação completa da API
- **[Exemplos Práticos FastAPI](FASTAPI_EXAMPLES.md)** - Exemplos de código para integração

### 🎛️ Guias Específicos
- **[Guia do Django Dashboard](DJANGO_DASHBOARD_GUIDE.md)** - Interface administrativa e relatórios
- **[Guia do Desenvolvedor](DEVELOPER_GUIDE.md)** - Arquitetura e desenvolvimento

## 🏗️ Visão Geral do Sistema

### Arquitetura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   SQL Server    │    │   Django        │
│   Collector     │◄──►│   Database      │◄──►│   Dashboard     │
│   (Porta 8001)  │    │   (Compartilhado)│    │   (Porta 8000)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes Principais
- **FastAPI Collector**: API para coleta de respostas via endpoints REST
- **Django Dashboard**: Interface administrativa com gráficos e relatórios
- **SQL Server**: Banco de dados compartilhado entre as aplicações
- **Templates HTML**: Interface web com Bootstrap e Chart.js

## 🚀 Início Rápido

### 1. Instalação
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd survey_analytics

# Configure o ambiente
python scripts/setup_project.py

# Configure suas credenciais no arquivo .env
cp env.example .env
# Edite o arquivo .env com suas credenciais do SQL Server
```

### 2. Executar Aplicações
```bash
# Terminal 1 - Django Dashboard
cd dashboard
python manage.py runserver

# Terminal 2 - FastAPI Collector
cd collector
uvicorn main:app --reload --port 8001
```

### 3. Acessar Interfaces
- **Dashboard**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8001/docs

## 📊 Funcionalidades Principais

### FastAPI Collector
- ✅ **POST** `/api/nps/submit` - Enviar respostas NPS
- ✅ **GET** `/api/nps/results` - Listar resultados
- ✅ **GET** `/api/nps/summary` - Resumo agregado
- ✅ Validação automática de dados
- ✅ Integração com SQL Server

### Django Dashboard
- ✅ **Dashboard interativo** com gráficos
- ✅ **Gerenciamento** de pesquisas e respostas
- ✅ **Filtros avançados** para análise
- ✅ **Exportação** CSV e Excel
- ✅ **Interface administrativa** completa

## 🔧 Configuração

### Variáveis de Ambiente
```env
# Database Settings
DB_HOST=localhost
DB_PORT=1433
DB_NAME=survey_analytics
DB_USER=seu-usuario
DB_PASSWORD=sua-senha

# Django Settings
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Banco de Dados
```sql
-- Execute no SQL Server
CREATE DATABASE survey_analytics;
-- Use o script database/init.sql para configuração completa
```

## 📝 Exemplos de Uso

### Enviar Resposta NPS
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

### Obter Resumo NPS
```python
import requests

url = "http://localhost:8001/api/nps/summary"
response = requests.get(url)
data = response.json()

print(f"NPS Score: {data['average_nps']}")
print(f"Promotores: {data['promoters_percentage']}%")
```

## 🧪 Testes

### Testes Automatizados
```bash
# Testes Django
cd dashboard
python manage.py test

# Testes FastAPI
cd collector
pytest

# Teste de conexão
python scripts/test_db_connection.py
```

### Validação Manual
1. Acesse o dashboard
2. Crie uma pesquisa via admin
3. Envie uma resposta via FastAPI
4. Verifique os dados no dashboard

## 🐳 Docker

### Execução com Docker
```bash
# Usar Docker Compose
docker-compose up -d

# Verificar logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

## 📈 Monitoramento

### URLs de Monitoramento
- **Health Check FastAPI**: http://localhost:8001/health
- **Health Check Django**: http://localhost:8000/health
- **API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Logs
- **Django**: Console durante desenvolvimento
- **FastAPI**: Console com nível DEBUG
- **Produção**: Configure logging apropriado

## 🔒 Segurança

### Recomendações
1. **Rate Limiting**: Implemente para endpoints públicos
2. **Validação**: Todos os inputs são validados
3. **CORS**: Configurado para desenvolvimento
4. **HTTPS**: Use em produção
5. **Autenticação**: Implemente JWT se necessário

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

### Padrões de Código
- Use Black para formatação
- Use Flake8 para linting
- Documente funções complexas
- Use type hints

## 📞 Suporte

### Recursos de Ajuda
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/survey_analytics/issues)
- **Documentação**: Consulte os arquivos em `docs/`
- **Exemplos**: Veja `docs/FASTAPI_EXAMPLES.md`

### Informações para Suporte
Ao solicitar suporte, inclua:
1. Sistema operacional e versão
2. Versão do Python
3. Versão do SQL Server
4. Logs de erro completos
5. Passos para reproduzir o problema

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🗺️ Roadmap

### Próximas Funcionalidades
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Cache Redis
- [ ] Notificações por email
- [ ] API para CSAT e CES
- [ ] Dashboard em tempo real
- [ ] Integração com Slack/Teams

---

*Última atualização: Janeiro 2024*

**Versão da Documentação**: 1.0.0
