#!/usr/bin/env python3
"""
Script para exportar o preview do email em PDF e PNG
"""
import os
import sys
from pathlib import Path
from datetime import datetime

def export_to_pdf_weasyprint(html_file, output_pdf):
    """Exporta HTML para PDF usando weasyprint"""
    try:
        from weasyprint import HTML
        print("Exportando para PDF usando WeasyPrint...")
        HTML(filename=html_file).write_pdf(output_pdf)
        print(f"✅ PDF criado: {output_pdf}")
        return True
    except ImportError:
        print("❌ WeasyPrint não instalado. Instalando...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint", "--quiet"])
            print("✅ WeasyPrint instalado!")
            from weasyprint import HTML
            HTML(filename=html_file).write_pdf(output_pdf)
            print(f"✅ PDF criado: {output_pdf}")
            return True
        except Exception as e:
            print(f"❌ Erro ao instalar/usar WeasyPrint: {e}")
            return False
    except Exception as e:
        print(f"❌ Erro ao criar PDF: {e}")
        return False

def export_to_pdf_playwright(html_file, output_pdf):
    """Exporta HTML para PDF usando playwright (alternativa)"""
    try:
        from playwright.sync_api import sync_playwright
        print("Exportando para PDF usando Playwright...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(html_file)}")
            page.pdf(path=output_pdf, format='A4', print_background=True)
            browser.close()
        
        print(f"✅ PDF criado: {output_pdf}")
        return True
    except ImportError:
        print("❌ Playwright não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro ao criar PDF com Playwright: {e}")
        return False

def export_to_png_playwright(html_file, output_png):
    """Exporta HTML para PNG usando playwright"""
    try:
        from playwright.sync_api import sync_playwright
        print("Exportando para PNG usando Playwright...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{os.path.abspath(html_file)}")
            page.screenshot(path=output_png, full_page=True)
            browser.close()
        
        print(f"✅ PNG criado: {output_png}")
        return True
    except ImportError:
        print("❌ Playwright não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro ao criar PNG: {e}")
        return False

def export_to_png_selenium(html_file, output_png):
    """Exporta HTML para PNG usando selenium (alternativa)"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("Exportando para PNG usando Selenium...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"file://{os.path.abspath(html_file)}")
        driver.save_screenshot(output_png)
        driver.quit()
        
        print(f"✅ PNG criado: {output_png}")
        return True
    except ImportError:
        print("❌ Selenium não instalado")
        return False
    except Exception as e:
        print(f"❌ Erro ao criar PNG: {e}")
        return False

def main():
    print("=" * 60)
    print("Exportador de Preview de Email - NPS Surveys")
    print("=" * 60)
    print()
    
    # Caminhos
    script_dir = Path(__file__).resolve().parent
    # Se estamos em pesquisas_nps/pesquisas_nps, subir um nível
    if script_dir.name == "pesquisas_nps" and (script_dir.parent / "pesquisas_nps").exists():
        base_dir = script_dir
    else:
        base_dir = script_dir / "pesquisas_nps"
    
    html_file = base_dir / "preview_email_convite.html"
    output_dir = base_dir / "exports"
    
    # Criar diretório de exports
    output_dir.mkdir(exist_ok=True)
    
    # Verificar se arquivo HTML existe
    if not html_file.exists():
        print(f"❌ Arquivo não encontrado: {html_file}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_pdf = output_dir / f"preview_email_convite_{timestamp}.pdf"
    output_png = output_dir / f"preview_email_convite_{timestamp}.png"
    
    print(f"Arquivo HTML: {html_file}")
    print(f"Diretório de saída: {output_dir}")
    print()
    
    # Tentar exportar para PDF
    print("Tentando exportar para PDF...")
    success_pdf = False
    
    # Método 1: WeasyPrint (mais simples)
    if not success_pdf:
        success_pdf = export_to_pdf_weasyprint(str(html_file), str(output_pdf))
    
    # Método 2: Playwright (alternativa)
    if not success_pdf:
        print("\nTentando método alternativo (Playwright)...")
        success_pdf = export_to_pdf_playwright(str(html_file), str(output_pdf))
    
    # Tentar exportar para PNG
    print("\nTentando exportar para PNG...")
    success_png = False
    
    # Método 1: Playwright
    if not success_png:
        success_png = export_to_png_playwright(str(html_file), str(output_png))
    
    # Método 2: Selenium (alternativa)
    if not success_png:
        print("\nTentando método alternativo (Selenium)...")
        success_png = export_to_png_selenium(str(html_file), str(output_png))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DA EXPORTAÇÃO")
    print("=" * 60)
    
    if success_pdf:
        print(f"✅ PDF: {output_pdf}")
        print(f"   Tamanho: {output_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("❌ PDF: Não foi possível criar")
    
    if success_png:
        print(f"✅ PNG: {output_png}")
        print(f"   Tamanho: {output_png.stat().st_size / 1024:.2f} KB")
    else:
        print("❌ PNG: Não foi possível criar")
    
    print()
    
    if success_pdf or success_png:
        print("📁 Arquivos salvos em:", output_dir)
        print("\n💡 Dica: Você pode compartilhar esses arquivos com sua equipe!")
        return True
    else:
        print("⚠️  Nenhum arquivo foi criado.")
        print("\n💡 Para exportar, você precisa instalar uma das bibliotecas:")
        print("   - weasyprint (para PDF)")
        print("   - playwright (para PDF e PNG)")
        print("   - selenium (para PNG)")
        print("\n   Execute: pip install weasyprint")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nExportação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

