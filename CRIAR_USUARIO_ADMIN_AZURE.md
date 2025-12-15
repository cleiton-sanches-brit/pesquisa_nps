# 📋 Guia Completo: Criar Usuário Admin no Azure App Service

Este documento fornece instruções detalhadas para criar um usuário administrador no portal Django (`/admin/`) quando a aplicação está hospedada no Azure App Service.

---

## 🔍 Entendendo a Situação

### Por que preciso criar um novo usuário?

- **Localmente**: Você usa SQLite (arquivo `db.sqlite3`) com usuário `admin`
- **No Azure**: A aplicação usa SQL Server (banco remoto) que é **completamente separado**
- **Conclusão**: O usuário criado localmente **NÃO** estará disponível no Azure

### Onde os usuários são armazenados?

Os usuários do Django (incluindo administradores) são armazenados na tabela `auth_user` do banco de dados. Como são bancos diferentes, você precisa criar um novo usuário no Azure.

---

## ✅ Pré-requisitos

Antes de criar o usuário admin, certifique-se de que:

1. ✅ A aplicação está deployada no Azure App Service
2. ✅ As migrações foram executadas (`python manage.py migrate`)
3. ✅ Você tem acesso ao Azure Portal ou Azure CLI
4. ✅ O banco de dados está configurado e acessível

---

## 🚀 Método 1: Via Console/SSH do Azure Portal (RECOMENDADO)

Este é o método mais simples e direto.

### Passo 1: Acessar o Console do App Service

1. Acesse o [Azure Portal](https://portal.azure.com)
2. Navegue até seu **App Service** (ex: `pesquisas-nps`)
3. No menu lateral, procure por:
   - **"SSH"** ou
   - **"Console"** ou
   - **"Advanced Tools"** → **"Go"** → **"SSH"**

### Passo 2: Navegar até a pasta do Django

No console, execute:

```bash
cd django_app
```

**Nota**: Se a pasta tiver outro nome, ajuste o comando. O caminho padrão é `/home/site/wwwroot/django_app`

### Passo 3: Verificar se as migrações foram executadas

```bash
python manage.py showmigrations
```

Se houver migrações pendentes, execute:

```bash
python manage.py migrate
```

### Passo 4: Criar o Superusuário

Execute o comando:

```bash
python manage.py createsuperuser
```

### Passo 5: Preencher os dados

O Django solicitará as seguintes informações:

```
Username: [digite o nome de usuário, ex: admin]
Email address: [digite o email, ex: admin@example.com]
Password: [digite a senha - não aparecerá na tela]
Password (again): [confirme a senha]
```

**Exemplo:**
```
Username: admin
Email address: admin@br-itsoftware.com.br
Password: ********
Password (again): ********
```

### Passo 6: Confirmar criação

Se tudo estiver correto, você verá:

```
Superuser created successfully.
```

### Passo 7: Testar o acesso

1. Acesse a URL do seu App Service: `https://seu-app.azurewebsites.net/admin/`
2. Faça login com as credenciais criadas
3. Você deve ver o painel administrativo do Django

---

## 🔧 Método 2: Via Azure CLI

Se você tem o Azure CLI instalado e configurado, pode usar este método.

### Passo 1: Conectar via SSH

```bash
az webapp ssh --name nome-do-seu-app --resource-group nome-do-resource-group
```

**Exemplo:**
```bash
az webapp ssh --name pesquisas-nps --resource-group rg-pesquisas-nps
```

### Passo 2: Navegar e criar usuário

```bash
cd django_app
python manage.py migrate  # Se necessário
python manage.py createsuperuser
```

Siga as instruções interativas para criar o usuário.

---

## 🤖 Método 3: Criar via Script Python (Não Interativo)

Este método é útil para automação ou quando você não pode usar o modo interativo.

### Passo 1: Criar o script

No console do Azure, crie um arquivo temporário:

```bash
cd django_app
cat > criar_admin.py << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Configurações do usuário
USERNAME = 'admin'
EMAIL = 'admin@br-itsoftware.com.br'
PASSWORD = 'SuaSenhaSegura123!'  # ALTERE ESTA SENHA!

# Verificar se o usuário já existe
if User.objects.filter(username=USERNAME).exists():
    print(f'Usuário {USERNAME} já existe!')
    user = User.objects.get(username=USERNAME)
    user.set_password(PASSWORD)
    user.save()
    print(f'Senha do usuário {USERNAME} foi atualizada!')
else:
    # Criar novo superusuário
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f'Superusuário {USERNAME} criado com sucesso!')
EOF
```

### Passo 2: Editar o script

**⚠️ IMPORTANTE**: Antes de executar, edite o script e altere:
- `PASSWORD = 'SuaSenhaSegura123!'` → Use uma senha forte
- `USERNAME` e `EMAIL` se desejar

### Passo 3: Executar o script

```bash
python criar_admin.py
```

### Passo 4: Remover o script (opcional, por segurança)

```bash
rm criar_admin.py
```

---

## 🔐 Método 4: Usar Variáveis de Ambiente (Mais Seguro)

Este método usa variáveis de ambiente para não expor a senha no código.

### Passo 1: Configurar variáveis no Azure Portal

1. No Azure Portal, vá em **App Service** → **Configuration** → **Application settings**
2. Adicione as seguintes variáveis:

```
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@br-itsoftware.com.br
ADMIN_PASSWORD=SuaSenhaSegura123!
```

3. Clique em **Save**

### Passo 2: Criar script que usa variáveis de ambiente

No console do Azure:

```bash
cd django_app
cat > criar_admin_env.py << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nps_admin.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Obter valores das variáveis de ambiente
USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
PASSWORD = os.getenv('ADMIN_PASSWORD')

if not PASSWORD:
    print('ERRO: Variável ADMIN_PASSWORD não configurada!')
    exit(1)

# Verificar se o usuário já existe
if User.objects.filter(username=USERNAME).exists():
    print(f'Usuário {USERNAME} já existe! Atualizando senha...')
    user = User.objects.get(username=USERNAME)
    user.set_password(PASSWORD)
    user.save()
    print(f'Senha do usuário {USERNAME} foi atualizada!')
else:
    # Criar novo superusuário
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f'Superusuário {USERNAME} criado com sucesso!')
EOF
```

### Passo 3: Executar o script

```bash
python criar_admin_env.py
```

### Passo 4: Remover variáveis de ambiente (recomendado)

Após criar o usuário, remova a variável `ADMIN_PASSWORD` do Azure Portal por segurança.

---

## 🛠️ Troubleshooting (Solução de Problemas)

### Erro: "Command 'python' not found"

**Solução**: Use `python3` em vez de `python`:

```bash
python3 manage.py createsuperuser
```

### Erro: "ModuleNotFoundError: No module named 'django'"

**Solução**: Certifique-se de estar no ambiente virtual correto ou que o Django está instalado:

```bash
# Verificar instalação
pip list | grep Django

# Se não estiver instalado, instalar
pip install -r requirements.txt
```

### Erro: "django.db.utils.OperationalError"

**Solução**: Verifique a conexão com o banco de dados:

1. Verifique as variáveis de ambiente no Azure Portal:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`

2. Teste a conexão:
```bash
python manage.py dbshell
```

### Erro: "Table 'auth_user' doesn't exist"

**Solução**: Execute as migrações primeiro:

```bash
python manage.py migrate
```

### Erro: "Superuser already exists"

**Solução**: O usuário já existe. Você pode:
- Usar o usuário existente
- Alterar a senha (veja seção abaixo)
- Criar um usuário com nome diferente

---

## 🔄 Alterar Senha de Usuário Existente

Se você já tem um usuário admin e quer alterar a senha:

### Método 1: Via Django Shell

```bash
cd django_app
python manage.py shell
```

No shell Python:

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(username='admin')
user.set_password('NovaSenhaSegura123!')
user.save()
print('Senha alterada com sucesso!')
exit()
```

### Método 2: Via Comando Django

```bash
python manage.py changepassword admin
```

Siga as instruções para definir a nova senha.

---

## 📝 Checklist de Verificação

Use este checklist para garantir que tudo está configurado corretamente:

- [ ] Aplicação está deployada no Azure
- [ ] Migrações foram executadas (`python manage.py migrate`)
- [ ] Banco de dados está acessível
- [ ] Variáveis de ambiente estão configuradas no Azure Portal
- [ ] Superusuário foi criado com sucesso
- [ ] Consigo acessar `/admin/` no navegador
- [ ] Consigo fazer login com as credenciais criadas
- [ ] Consigo ver o painel administrativo

---

## 🔒 Boas Práticas de Segurança

1. **Use senhas fortes**: Mínimo de 12 caracteres, com letras, números e símbolos
2. **Não compartilhe credenciais**: Cada administrador deve ter seu próprio usuário
3. **Remova variáveis de ambiente**: Após criar o usuário, remova `ADMIN_PASSWORD` do Azure
4. **Use HTTPS**: Sempre acesse o admin via HTTPS
5. **Mude a senha regularmente**: Especialmente em ambientes de produção
6. **Limite acesso**: Crie usuários com permissões mínimas necessárias

---

## 📞 Suporte Adicional

Se encontrar problemas:

1. Verifique os logs do App Service: **App Service** → **Log stream**
2. Verifique os logs de aplicação: **App Service** → **Logs** → **Application Logs**
3. Teste a conexão com o banco: `python manage.py dbshell`
4. Verifique as variáveis de ambiente no Azure Portal

---

## 📚 Referências

- [Documentação Django - Creating Superusers](https://docs.djangoproject.com/en/stable/ref/django-admin/#createsuperuser)
- [Azure App Service - SSH](https://docs.microsoft.com/en-us/azure/app-service/configure-linux-open-ssh-session)
- [Azure CLI - webapp ssh](https://docs.microsoft.com/en-us/cli/azure/webapp/ssh)

---

**Última atualização**: 2024

