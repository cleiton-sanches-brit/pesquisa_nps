# 💻 Comandos CMD - Iniciar Servidor Django

## 🚀 Comando Rápido

### Opção 1: Usando o Script Batch (Mais Fácil)
```cmd
INICIAR_DJANGO_CMD.bat
```

### Opção 2: Comando Manual no CMD

**1. Navegar até o diretório:**
```cmd
cd pesquisas_nps\django_app
```

**2. Ativar ambiente virtual:**
```cmd
..\..\venv\Scripts\activate
```

**3. Iniciar servidor:**
```cmd
python manage.py runserver
```

### Opção 3: Comando Completo em Uma Linha
```cmd
cd pesquisas_nps\django_app && ..\..\venv\Scripts\python.exe manage.py runserver
```

---

## 📋 Passo a Passo Detalhado

### 1. Abrir CMD
- Pressione `Windows + R`
- Digite `cmd` e pressione Enter
- Ou pesquise "Prompt de Comando" no menu Iniciar

### 2. Navegar até o projeto
```cmd
cd C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps\pesquisas_nps\django_app
```

### 3. Ativar ambiente virtual
```cmd
..\..\venv\Scripts\activate
```

Você verá `(venv)` no início da linha quando ativado.

### 4. Iniciar servidor
```cmd
python manage.py runserver
```

### 5. Acessar
Abra o navegador em: `http://localhost:8000/admin/`

---

## ⚙️ Opções do Comando runserver

### Porta padrão (8000):
```cmd
python manage.py runserver
```

### Porta customizada:
```cmd
python manage.py runserver 8080
```

### IP específico:
```cmd
python manage.py runserver 0.0.0.0:8000
```

### Sem recarregar automaticamente:
```cmd
python manage.py runserver --noreload
```

---

## 🛑 Parar o Servidor

No CMD onde o servidor está rodando:
- Pressione `Ctrl + C`

---

## ✅ Verificar se está funcionando

Após iniciar, você verá:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🔧 Resolução de Problemas

### Erro: "python não é reconhecido"
**Solução:** Use o Python do venv:
```cmd
..\..\venv\Scripts\python.exe manage.py runserver
```

### Erro: "ModuleNotFoundError"
**Solução:** Certifique-se de que o venv está ativado e as dependências instaladas:
```cmd
..\..\venv\Scripts\pip.exe install -r ..\..\requirements.txt
```

### Erro: "Port already in use"
**Solução:** Use outra porta:
```cmd
python manage.py runserver 8001
```

---

## 📝 Comandos Úteis Adicionais

### Ver todas as rotas:
```cmd
python manage.py show_urls
```

### Criar superusuário:
```cmd
python manage.py createsuperuser
```

### Aplicar migrações:
```cmd
python manage.py migrate
```

### Criar migrações:
```cmd
python manage.py makemigrations
```

---

**Status**: ✅ Comandos documentados!

