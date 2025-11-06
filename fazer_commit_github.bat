@echo off
chcp 65001 >nul
echo 🔗 Configurando repositório GitHub...
echo.

cd /d "%~dp0pesquisas_nps"

REM Verificar se Git está disponível
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado no PATH!
    echo.
    echo Por favor:
    echo 1. Reinicie o terminal após instalar o Git
    echo 2. OU adicione Git ao PATH manualmente
    echo.
    pause
    exit /b 1
)

echo ✅ Git encontrado
echo.

REM Verificar se já é repositório Git
if not exist ".git" (
    echo 📦 Inicializando repositório Git...
    git init
)

REM Configurar remote
echo 🔗 Configurando remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/cleiton-sanches-brit/pesquisa_nps.git
echo ✅ Remote configurado
echo.

REM Verificar configuração do Git
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚙️  Configurando Git (primeira vez)...
    git config --global user.name "Cleiton Sanches"
    git config --global user.email "cleiton.sanches@exemplo.com"
    echo ✅ Git configurado
    echo.
)

REM Adicionar arquivos
echo 📝 Adicionando arquivos...
git add .
echo ✅ Arquivos adicionados
echo.

REM Fazer commit
echo 💾 Fazendo commit...
git commit -m "Commit inicial - Sistema de Pesquisas NPS"
echo ✅ Commit realizado
echo.

REM Renomear branch para main
echo 🌿 Configurando branch main...
git branch -M main
echo.

REM Push para GitHub
echo 📤 Enviando para GitHub...
echo.
echo ⚠️  IMPORTANTE: GitHub não aceita mais senha normal!
echo Você precisa usar um Personal Access Token.
echo.
echo Se ainda não tem um token:
echo 1. Acesse: https://github.com/settings/tokens
echo 2. Clique em "Generate new token (classic)"
echo 3. Marque a opção "repo" (acesso completo)
echo 4. Copie o token gerado
echo.
echo Quando pedir senha, cole o TOKEN (não sua senha)
echo.
pause

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ Código enviado para GitHub com sucesso!
    echo.
    echo 🔗 Repositório: https://github.com/cleiton-sanches-brit/pesquisa_nps
) else (
    echo.
    echo ❌ Erro ao fazer push.
    echo.
    echo Possíveis causas:
    echo - Token inválido ou expirado
    echo - Repositório não existe ou sem permissão
    echo - Problema de conexão
    echo.
    echo Tente novamente com um token válido.
)

echo.
pause

