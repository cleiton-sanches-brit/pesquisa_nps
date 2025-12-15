# 🔐 Configurar Push para britsoftware/PesquisaNPS

## ⚠️ Importante: GitHub não aceita senhas

O GitHub **não aceita mais senhas** para autenticação via Git. É necessário usar um **Personal Access Token (PAT)**.

---

## 📋 Passo a Passo

### 1. Criar Personal Access Token no GitHub

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Configure:
   - **Note**: `PesquisaNPS - Deploy`
   - **Expiration**: Escolha um prazo (ex: 90 dias ou No expiration)
   - **Scopes**: Marque pelo menos:
     - ✅ `repo` (acesso completo aos repositórios)
4. Clique em **"Generate token"**
5. **COPIE O TOKEN** (você só verá uma vez!)

### 2. Configurar o Remote

O remote `britsoftware` já está configurado. Se precisar reconfigurar:

```bash
git remote set-url britsoftware https://github.com/britsoftware/PesquisaNPS.git
```

### 3. Fazer Push usando o Token

**Opção A - Usar token na URL (temporário):**

```bash
git push https://csanches@br-itsoftware.com.br:SEU_TOKEN_AQUI@github.com/britsoftware/PesquisaNPS.git main
```

**Opção B - Git pedirá credenciais (recomendado):**

```bash
git push britsoftware main
```

Quando pedir:
- **Username**: `csanches@br-itsoftware.com.br`
- **Password**: Cole o **Personal Access Token** (não a senha!)

**Opção C - Usar Git Credential Manager (mais seguro):**

O Windows pode ter o Git Credential Manager instalado. Ao fazer push, ele abrirá uma janela para você inserir o token.

---

## 🚀 Comando Rápido

Após criar o token, execute:

```bash
cd C:\Users\CleitonSanchesBR-iT\Documents\Projetos_automacoes\pesquisas_nps
git push britsoftware main
```

Quando solicitado:
- Username: `csanches@br-itsoftware.com.br`
- Password: `[cole seu Personal Access Token aqui]`

---

## 🔒 Segurança

- ⚠️ **NUNCA** commite o token no código
- ⚠️ **NUNCA** compartilhe o token
- ✅ Use o Git Credential Manager para armazenar o token com segurança
- ✅ Configure expiração no token

---

## 📝 Verificar Remotes Configurados

```bash
git remote -v
```

Você deve ver:
```
britsoftware	https://github.com/britsoftware/PesquisaNPS.git (fetch)
britsoftware	https://github.com/britsoftware/PesquisaNPS.git (push)
origin	https://github.com/cleiton-sanches-brit/pesquisa_nps.git (fetch)
origin	https://github.com/cleiton-sanches-brit/pesquisa_nps.git (push)
```

---

## 🆘 Troubleshooting

### Erro: "Authentication failed"

- Verifique se está usando o **token** e não a senha
- Verifique se o token tem permissão `repo`
- Verifique se o token não expirou

### Erro: "Permission denied"

- Verifique se você tem acesso ao repositório `britsoftware/PesquisaNPS`
- Verifique se o token tem escopo `repo`

### Limpar credenciais salvas (se necessário)

```bash
git credential-manager-core erase
# ou
git credential reject https://github.com
```

---

**Nota**: O remote `britsoftware` já está configurado. Você só precisa criar o token e fazer o push.

