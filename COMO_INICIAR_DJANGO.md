# 🚀 Como Iniciar o Servidor Django

## 📋 Métodos para Iniciar

### Método 1: Script Automático (Recomendado)

Execute no PowerShell:
```powershell
.\iniciar_django.ps1
```

Este script:
- ✅ Verifica o ambiente virtual
- ✅ Inicia o servidor na porta 8000
- ✅ Mostra as URLs importantes

### Método 2: Manual (Passo a Passo)

1. **Abra o PowerShell** no diretório do projeto

2. **Navegue até o django_app**:
   ```powershell
   cd django_app
   ```

3. **Inicie o servidor**:
   ```powershell
   ..\venv\Scripts\python.exe manage.py runserver
   ```

4. **Acesse no navegador**:
   - http://localhost:8000
   - http://localhost:8000/admin/

### Método 3: Usando o Script Completo (Django + FastAPI)

Execute:
```powershell
.\iniciar_corrigido.ps1
```

Este script inicia ambos os serviços (Django e FastAPI).

## ✅ Verificar se Está Rodando

Após iniciar, você verá algo como:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🌐 URLs Importantes

Após iniciar o servidor:

- **Home**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **Lista de Convites**: http://localhost:8000/survey/1/invitations/
- **Enviar Convites**: http://localhost:8000/survey/1/invite/
- **Responder Pesquisa**: http://localhost:8000/survey/1/respond/[TOKEN]/

## 🛑 Parar o Servidor

Pressione: **Ctrl + C** no terminal onde o servidor está rodando.

## ⚠️ Problemas Comuns

### Erro: "Port 8000 is already in use"
**Solução**: Altere a porta:
```powershell
..\venv\Scripts\python.exe manage.py runserver 8001
```

### Erro: "No module named 'django'"
**Solução**: Ative o ambiente virtual:
```powershell
.\venv\Scripts\activate
```

### Erro: "ModuleNotFoundError"
**Solução**: Instale as dependências:
```powershell
pip install -r requirements.txt
```

## 📝 Credenciais do Admin

- **Usuário**: admin
- **Senha**: admin123

---

**Pronto!** Agora você pode testar os templates! 🎉
