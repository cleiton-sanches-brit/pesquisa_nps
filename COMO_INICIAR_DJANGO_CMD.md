# 🚀 Como Iniciar o Servidor Django - CMD (Prompt de Comando)

## 📋 Métodos para Iniciar

### Método 1: Arquivo Batch (Mais Fácil) ✅

**Duplo clique** no arquivo:
```
INICIAR_DJANGO_CMD.bat
```

Ou execute no CMD:
```cmd
INICIAR_DJANGO_CMD.bat
```

### Método 2: Comandos Manuais (Passo a Passo)

1. **Abra o CMD (Prompt de Comando)**

2. **Navegue até o diretório do projeto**:
   ```cmd
   cd C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps
   ```

3. **Entre no diretório django_app**:
   ```cmd
   cd django_app
   ```

4. **Inicie o servidor**:
   ```cmd
   ..\venv\Scripts\python.exe manage.py runserver
   ```

5. **Aguarde a mensagem**:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

## ✅ Sequência Completa de Comandos (Copiar e Colar)

```cmd
cd C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps
cd django_app
..\venv\Scripts\python.exe manage.py runserver
```

## 🌐 URLs Importantes

Após iniciar o servidor:

- **Home**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/
- **Lista de Convites**: http://localhost:8000/survey/1/invitations/
- **Enviar Convites**: http://localhost:8000/survey/1/invite/
- **Responder Pesquisa**: http://localhost:8000/survey/1/respond/7ff55155-1afa-45ba-bc2a-0848a1963e68/

## 🛑 Parar o Servidor

Pressione: **Ctrl + C** no CMD onde o servidor está rodando.

## ⚠️ Problemas Comuns

### Erro: "Port 8000 is already in use"
**Solução**: Altere a porta:
```cmd
..\venv\Scripts\python.exe manage.py runserver 8001
```

### Erro: "'python' não é reconhecido"
**Solução**: Use o caminho completo do Python do venv:
```cmd
..\venv\Scripts\python.exe
```

### Erro: "No module named 'django'"
**Solução**: Verifique se está usando o Python do venv:
```cmd
..\venv\Scripts\python.exe manage.py runserver
```

## 📝 Credenciais do Admin

- **Usuário**: admin
- **Senha**: admin123

## 🎯 Exemplo de Uso Rápido

1. Abra o CMD
2. Digite:
   ```cmd
   cd /d C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\django_app
   ```
3. Digite:
   ```cmd
   ..\venv\Scripts\python.exe manage.py runserver
   ```
4. Abra o navegador em: http://localhost:8000

---

**Pronto para usar!** 🎉
