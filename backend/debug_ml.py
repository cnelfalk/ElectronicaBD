import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.scrapers_especificaciones import MercadoLibreScraper

class DebugMLScraper(MercadoLibreScraper):
    def ejecutarScraping(self):
        url = f"https://listado.mercadolibre.com.ar/computacion/laptops-accesorios/notebooks/{self.marca.lower()}"
        print(f"[DEBUG] Navegando a: {url}")
        driver = self._crearDriver()
        try:
            driver.get(url)
            print("[DEBUG] Esperando 6 segundos...")
            import time
            time.sleep(6)
            
            html = driver.page_source
            with open("ml_debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[DEBUG] Pagina guardada en ml_debug.html (Longitud: {len(html)} caracteres)")
            
            from bs4 import BeautifulSoup
            sopa = BeautifulSoup(html, 'html.parser')
            items = sopa.find_all('li', class_='ui-search-layout__item')
            print(f"[DEBUG] Cantidad de items encontrados con 'ui-search-layout__item': {len(items)}")
            
            # Si no hay, busquemos que selectores alternativos hay
            if not items:
                title = sopa.find('title')
                print(f"[DEBUG] Titulo de la pagina: {title.text if title else 'Sin titulo'}")
                # Ver si hay algun indicio de captcha
                if "captcha" in html.lower() or "robot" in html.lower() or "human" in html.lower() or "cloudflare" in html.lower():
                    print("[DEBUG] ¡ALERTA! Se detecto presencia de palabras de captcha/bloqueo de bots.")
        finally:
            driver.quit()

if __name__ == "__main__":
    scraper = DebugMLScraper("Asus")
    scraper.ejecutarScraping()
