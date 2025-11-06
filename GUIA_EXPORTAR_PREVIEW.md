# 📄 Guia: Exportar Preview de Email

## 📋 Como Exportar o Preview de Email

Você pode exportar o preview do email em **PDF** ou **PNG** para compartilhar com sua equipe.

## 🚀 Métodos Rápidos

### Opção 1: Batch Script (Windows)
```batch
EXPORTAR_PREVIEW_EMAIL.bat
```

### Opção 2: PowerShell Script
```powershell
.\EXPORTAR_PREVIEW_EMAIL.ps1
```

### Opção 3: Python Direto
```bash
cd pesquisas_nps
python exportar_preview_email.py
```

## 📦 Instalação da Biblioteca (se necessário)

Se você receber erro de biblioteca não encontrada:

```bash
pip install weasyprint
```

Ou usando o venv:
```bash
venv\Scripts\python.exe -m pip install weasyprint
```

## 📁 Onde os Arquivos são Salvos

Os arquivos exportados são salvos em:
```
pesquisas_nps/exports/
```

Os arquivos terão nomes como:
- `preview_email_convite_20251129_143022.pdf`
- `preview_email_convite_20251129_143022.png`

## 📄 Formatos Disponíveis

### PDF (Recomendado)
- ✅ Formato profissional
- ✅ Fácil de compartilhar
- ✅ Mantém formatação
- ✅ Tamanho pequeno

### PNG
- ✅ Imagem visual
- ✅ Fácil de visualizar
- ✅ Pode ser inserido em documentos

## 🔧 Resolução de Problemas

### Erro: "weasyprint não encontrado"
**Solução:**
```bash
pip install weasyprint
```

### Erro: "Não foi possível criar PDF"
**Soluções alternativas:**

1. **Usar método manual no navegador:**
   - Abra `preview_email_convite.html` no navegador
   - Pressione `Ctrl+P` (ou Cmd+P no Mac)
   - Escolha "Salvar como PDF"

2. **Usar ferramenta online:**
   - Acesse: https://www.ilovepdf.com/html-to-pdf
   - Faça upload do arquivo HTML
   - Converta para PDF

### Erro: "Playwright não encontrado"
O script tentará usar WeasyPrint primeiro. Se precisar de Playwright:
```bash
pip install playwright
playwright install chromium
```

## 💡 Dicas

### Para Compartilhar com o Time:

1. **PDF** - Melhor para documentos e apresentações
2. **PNG** - Melhor para visualização rápida e inserção em emails

### Exportação Manual (Alternativa Simples):

Se o script não funcionar, você pode:

1. Abrir `preview_email_convite.html` no navegador
2. Pressionar `Ctrl+P` (Imprimir)
3. Escolher "Salvar como PDF"
4. Ou usar extensões de navegador como "Print Friendly"

## 📊 Exemplo de Uso

```bash
# 1. Executar exportação
python exportar_preview_email.py

# 2. Verificar arquivos criados
cd exports
dir

# 3. Compartilhar com equipe
# Envie o arquivo PDF ou PNG por email/Slack/etc
```

## ✅ Checklist

- [ ] Biblioteca weasyprint instalada
- [ ] Script executado com sucesso
- [ ] Arquivo PDF/PNG criado na pasta `exports/`
- [ ] Arquivo compartilhado com equipe para validação

---

**Status**: ✅ Script de exportação criado e pronto para uso!

