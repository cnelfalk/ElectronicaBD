import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from bs4 import BeautifulSoup
from scrapers.scraper_base import ScraperBase


class AMDScraperCPU(ScraperBase):
    """
    Scraper de especificaciones de procesadores AMD desde amd.com.
    Fuente: https://www.amd.com/es/products/processors/laptop
    Guarda CPUs con precio=0 (no son vendidos directamente por AMD).
    """

    URL = "https://www.amd.com/es/products/processors/laptop"

    def __init__(self):
        super().__init__("AMD")

    def ejecutarScraping(self):
        print(f"  [AMD] Accediendo al catálogo de CPUs: {self.URL}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL)
            print("  [AMD] Esperando renderizado JS...")
            time.sleep(6)

            sopa = BeautifulSoup(driver.page_source, 'lxml')

            # AMD lista sus CPUs en filas de tabla o tarjetas con clase 'product-card'
            items = (
                sopa.find_all('tr', class_=lambda c: c and 'product' in c.lower()) or
                sopa.find_all('div', class_=lambda c: c and 'product-card' in c.lower()) or
                sopa.find_all('div', class_='field--type-entity-reference')
            )

            print(f"  [AMD] {len(items)} procesadores encontrados.")
            if not items:
                print("  [AMD] Sin resultados. AMD puede haber cambiado su estructura HTML.")
                return

            for item in items[:15]:
                try:
                    # Nombre del procesador
                    nombre_tag = item.find('h3') or item.find('h4') or item.find('td', class_=lambda c: c and 'name' in c.lower())
                    if not nombre_tag:
                        continue
                    nombre = nombre_tag.text.strip()
                    if not any(k in nombre for k in ["Ryzen", "EPYC", "Athlon"]):
                        continue

                    modelo = f"AMD {nombre}" if "AMD" not in nombre else nombre

                    # Extraer specs del texto completo del ítem
                    texto = item.get_text(separator=" ")

                    nucleos = self._extraerNumero(texto, r'(\d+)\s*núcleos?') or self._extraerNumero(texto, r'(\d+)\s*cores?') or 6
                    hilos = self._extraerNumero(texto, r'(\d+)\s*hilos?') or self._extraerNumero(texto, r'(\d+)\s*threads?') or nucleos * 2
                    frecBase = self._extraerDecimal(texto, r'(\d+[.,]\d+)\s*ghz') or 3.0
                    tdp = self._extraerNumero(texto, r'(\d+)\s*w\b') or 65

                    enlace_tag = item.find('a')
                    urlCpu = f"https://www.amd.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else self.URL

                    self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecBase + 1.0, tdp, urlCpu)
                    print(f"  [AMD] Guardado: {modelo[:60]}")
                    self._esperar()

                except Exception as e:
                    print(f"  [AMD] Error en procesador: {e}")

        finally:
            driver.quit()

    def _extraerNumero(self, texto, patron):
        import re
        m = re.search(patron, texto, re.IGNORECASE)
        return int(m.group(1)) if m else None

    def _extraerDecimal(self, texto, patron):
        import re
        m = re.search(patron, texto, re.IGNORECASE)
        return float(m.group(1).replace(',', '.')) if m else None


class IntelScraperCPU(ScraperBase):
    """
    Scraper de especificaciones de procesadores Intel desde ark.intel.com.
    Fuente: https://ark.intel.com/content/www/us/en/ark/search.html?q=core+i
    Guarda CPUs con precio=0 (Intel no vende directamente al consumidor).
    """

    URL = "https://ark.intel.com/content/www/us/en/ark/search.html?q=core+i&s=t&OrderBy=Featured"

    def __init__(self):
        super().__init__("Intel")

    def ejecutarScraping(self):
        print(f"  [INTEL] Accediendo al catálogo ARK de Intel: {self.URL}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL)
            print("  [INTEL] Esperando renderizado JS...")
            time.sleep(7)

            sopa = BeautifulSoup(driver.page_source, 'lxml')

            # ARK de Intel lista productos en tabla con clase 'result-list' o similar
            items = (
                sopa.find_all('div', class_='result-list-item') or
                sopa.find_all('tr', class_=lambda c: c and 'result' in c.lower()) or
                sopa.find_all('li', class_=lambda c: c and 'product' in c.lower())
            )

            print(f"  [INTEL] {len(items)} procesadores encontrados.")
            if not items:
                print("  [INTEL] Sin resultados. El ARK de Intel puede requerir ajuste de selectores.")
                return

            for item in items[:15]:
                try:
                    nombre_tag = item.find('h3') or item.find('a', class_=lambda c: c and 'product' in c.lower()) or item.find('td')
                    if not nombre_tag:
                        continue
                    nombre = nombre_tag.text.strip()
                    if "Core" not in nombre and "Xeon" not in nombre:
                        continue

                    modelo = f"Intel {nombre}" if "Intel" not in nombre else nombre

                    texto = item.get_text(separator=" ")
                    nucleos = self._extraerNumero(texto, r'(\d+)\s*(?:núcleos?|cores?)') or 4
                    hilos = self._extraerNumero(texto, r'(\d+)\s*(?:hilos?|threads?)') or nucleos * 2
                    frecBase = self._extraerDecimal(texto, r'(\d+[.,]\d+)\s*ghz') or 3.0
                    tdp = self._extraerNumero(texto, r'(\d+)\s*w\b') or 65

                    enlace_tag = item.find('a')
                    urlCpu = f"https://ark.intel.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else self.URL

                    self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecBase + 0.8, tdp, urlCpu)
                    print(f"  [INTEL] Guardado: {modelo[:60]}")
                    self._esperar()

                except Exception as e:
                    print(f"  [INTEL] Error en procesador: {e}")

        finally:
            driver.quit()

    def _extraerNumero(self, texto, patron):
        import re
        m = re.search(patron, texto, re.IGNORECASE)
        return int(m.group(1)) if m else None

    def _extraerDecimal(self, texto, patron):
        import re
        m = re.search(patron, texto, re.IGNORECASE)
        return float(m.group(1).replace(',', '.')) if m else None
