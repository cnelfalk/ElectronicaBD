import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
from bs4 import BeautifulSoup
from scrapers.scraper_base import ScraperBase


class AMDScraperCPU(ScraperBase):
    """
    Scraper de especificaciones de procesadores AMD desde amd.com.
    Fuente: https://www.amd.com/es/products/processors/laptop.html
    Guarda CPUs con precio=0 (no son vendidos directamente por AMD).

    Estrategia:
    1. Navegar a la pagina de procesadores laptop con --disable-http2 (evita ERR_HTTP2_PROTOCOL_ERROR)
    2. Extraer los enlaces a subpaginas de familias Ryzen
    3. Parsear nombres y specs de cada enlace encontrado
    """

    URL = "https://www.amd.com/es/products/processors/laptop.html"

    def __init__(self):
        super().__init__("AMD")

    def ejecutarScraping(self):
        print(f"  [AMD] Accediendo al catalogo de CPUs: {self.URL}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL)
            print("  [AMD] Esperando renderizado JS...")
            time.sleep(6)

            # Scrollear para activar lazy loading
            for i in range(3):
                driver.execute_script(f"window.scrollTo(0, {(i + 1) * 1500});")
                time.sleep(1)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')

            # Estrategia 1: Buscar en tablas de producto o tarjetas
            items = (
                sopa.find_all('tr', class_=lambda c: c and 'product' in c.lower()) or
                sopa.find_all('div', class_=lambda c: c and 'product-card' in c.lower()) or
                sopa.find_all('div', class_='field--type-entity-reference')
            )

            if items:
                print(f"  [AMD] {len(items)} procesadores encontrados en tablas/cards.")
                self._procesarItems(items)
                return

            # Estrategia 2: Extraer enlaces a subpaginas de familias Ryzen
            print("  [AMD] Sin tablas de producto. Buscando enlaces a familias Ryzen...")
            ryzen_links = []
            for a in sopa.find_all('a', href=True):
                href = a.get('href', '')
                texto = a.text.strip()
                # Buscar enlaces a paginas de familias Ryzen para laptops
                if ('ryzen' in href.lower() or 'ryzen' in texto.lower()) and 'laptop' in href.lower():
                    url_completa = href if href.startswith('http') else f"https://www.amd.com{href}"
                    if url_completa not in [rl[1] for rl in ryzen_links]:
                        ryzen_links.append((texto, url_completa))

            if ryzen_links:
                print(f"  [AMD] {len(ryzen_links)} familias Ryzen encontradas.")
                productosGuardados = 0
                for nombre_familia, url_familia in ryzen_links[:5]:
                    guardados = self._scrapearFamiliaRyzen(driver, nombre_familia, url_familia)
                    productosGuardados += guardados

                if productosGuardados > 0:
                    print(f"  [AMD] Extraccion completada: {productosGuardados} CPUs guardados.")
                    return

            # Estrategia 3: Extraer modelos directamente de los textos de la pagina
            print("  [AMD] Intentando extraccion directa de modelos del texto de la pagina...")
            productosGuardados = self._extraerModelosDeTexto(sopa)
            print(f"  [AMD] Extraccion completada: {productosGuardados} CPUs guardados.")

        finally:
            driver.quit()

    def _procesarItems(self, items):
        """Procesa items encontrados en tablas o cards de producto."""
        productosGuardados = 0
        for item in items[:15]:
            try:
                nombre_tag = item.find('h3') or item.find('h4') or item.find('td', class_=lambda c: c and 'name' in c.lower())
                if not nombre_tag:
                    continue
                nombre = nombre_tag.text.strip()
                if not any(k in nombre for k in ["Ryzen", "EPYC", "Athlon"]):
                    continue

                modelo = f"AMD {nombre}" if "AMD" not in nombre else nombre
                texto = item.get_text(separator=" ")

                nucleos = self._extraerNumero(texto, r'(\d+)\s*nucleos?') or self._extraerNumero(texto, r'(\d+)\s*cores?') or 6
                hilos = self._extraerNumero(texto, r'(\d+)\s*hilos?') or self._extraerNumero(texto, r'(\d+)\s*threads?') or nucleos * 2
                frecBase = self._extraerDecimal(texto, r'(\d+[.,]\d+)\s*ghz') or 3.0
                tdp = self._extraerNumero(texto, r'(\d+)\s*w\b') or 65

                enlace_tag = item.find('a')
                urlCpu = f"https://www.amd.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else self.URL

                self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecBase + 1.0, tdp, urlCpu)
                print(f"  [AMD] Guardado: {modelo[:60]}")
                productosGuardados += 1
                self._esperar()

            except Exception as e:
                print(f"  [AMD] Error en procesador: {e}")

        print(f"  [AMD] Total guardados desde items: {productosGuardados}")

    def _scrapearFamiliaRyzen(self, driver, nombre_familia, url_familia):
        """Navega a una subpagina de familia Ryzen y extrae los modelos de CPU."""
        try:
            print(f"  [AMD]   -> Visitando familia: {nombre_familia[:50]} ({url_familia[:70]}...)")
            driver.get(url_familia)
            time.sleep(4)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            texto_pagina = sopa.get_text(separator=" ").lower()

            # Buscar modelos Ryzen en el texto
            modelos = re.findall(
                r'(amd\s+)?ryzen\s+(\d+)\s+(\d{4}\w*)',
                texto_pagina, re.IGNORECASE
            )

            guardados = 0
            vistos = set()
            for _, serie, modelo_num in modelos[:15]:
                modelo = f"AMD Ryzen {serie} {modelo_num.upper()}"
                if modelo in vistos:
                    continue
                vistos.add(modelo)

                # Estimar specs basicas por serie
                nucleos, tdp = self._estimarSpecsPorSerie(serie, modelo_num)
                hilos = nucleos * 2
                frecBase = 3.0

                # Buscar frecuencia en contexto cercano
                freq_match = re.search(
                    rf'ryzen\s+{serie}\s+{modelo_num}\D{{0,30}}?(\d+[.,]\d+)\s*ghz',
                    texto_pagina, re.IGNORECASE
                )
                if freq_match:
                    frecBase = float(freq_match.group(1).replace(',', '.'))

                self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecBase + 1.0, tdp, url_familia)
                print(f"  [AMD]   Guardado: {modelo} | {nucleos}C/{hilos}T | {frecBase}GHz")
                guardados += 1

            return guardados

        except Exception as e:
            print(f"  [AMD]   Error en familia {nombre_familia[:40]}: {e}")
            return 0

    def _extraerModelosDeTexto(self, sopa):
        """Extrae modelos Ryzen directamente del texto de la pagina principal."""
        texto = sopa.get_text(separator=" ")

        # Buscar todos los modelos Ryzen mencionados en la pagina
        modelos = re.findall(
            r'(?:AMD\s+)?Ryzen\s+(\d+)\s+(\d{4}\w*)',
            texto, re.IGNORECASE
        )

        guardados = 0
        vistos = set()
        for serie, modelo_num in modelos[:15]:
            modelo = f"AMD Ryzen {serie} {modelo_num.upper()}"
            if modelo in vistos:
                continue
            vistos.add(modelo)

            nucleos, tdp = self._estimarSpecsPorSerie(serie, modelo_num)
            hilos = nucleos * 2
            frecBase = 3.0

            self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecBase + 1.0, tdp, self.URL)
            print(f"  [AMD] Guardado (texto): {modelo}")
            guardados += 1

        return guardados

    def _estimarSpecsPorSerie(self, serie, modelo_num):
        """Estima nucleos y TDP basado en la serie Ryzen."""
        serie = str(serie)
        modelo_upper = modelo_num.upper()
        # Detectar si es HX/H (alto rendimiento) o U (bajo consumo)
        es_alto_rendimiento = modelo_upper.endswith('HX') or modelo_upper.endswith('H') or modelo_upper.endswith('HS')

        if serie == '9':
            nucleos = 16 if es_alto_rendimiento else 8
            tdp = 55 if es_alto_rendimiento else 28
        elif serie == '7':
            nucleos = 8
            tdp = 45 if es_alto_rendimiento else 28
        elif serie == '5':
            nucleos = 6
            tdp = 45 if es_alto_rendimiento else 15
        elif serie == '3':
            nucleos = 4
            tdp = 35 if es_alto_rendimiento else 15
        else:
            nucleos = 6
            tdp = 28

        return nucleos, tdp

    def _extraerNumero(self, texto, patron):
        m = re.search(patron, texto, re.IGNORECASE)
        return int(m.group(1)) if m else None

    def _extraerDecimal(self, texto, patron):
        m = re.search(patron, texto, re.IGNORECASE)
        return float(m.group(1).replace(',', '.')) if m else None


class IntelScraperCPU(ScraperBase):
    """
    Scraper de especificaciones de procesadores Intel desde ARK.
    Fuente: https://ark.intel.com/content/www/us/en/ark.html

    Estrategia:
    1. Navegar al indice principal de ARK
    2. Extraer enlaces de series de procesadores Core recientes (11th-14th gen, Ultra, Series 1-3)
    3. Visitar cada serie y parsear la tabla estatica de productos
       (columnas: Product Name, Launch Date, Total Cores, Max Turbo Frequency, Cache, GPU)
    """

    URL_ARK = "https://ark.intel.com/content/www/us/en/ark.html"

    # Series recientes que nos interesan (generaciones 11+, Ultra, Series 1-3)
    SERIES_KEYWORDS = [
        '13th-generation-intel-core-i7',
        '13th-generation-intel-core-i5',
        '14th-gen',
        'intel-core-ultra-processors-series-2',
        'intel-core-ultra-processors-series-1',
        'intel-core-processors-series-3',
        'intel-core-processors-series-2',
        'intel-core-processors-series-1',
        '12th-generation-intel-core-i7',
        '12th-generation-intel-core-i5',
    ]

    def __init__(self):
        super().__init__("Intel")

    def ejecutarScraping(self):
        print(f"  [INTEL] Accediendo al indice ARK: {self.URL_ARK}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL_ARK)
            print("  [INTEL] Esperando renderizado JS del indice...")
            time.sleep(6)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')

            # Extraer enlaces de series que nos interesan
            series_urls = []
            for a in sopa.find_all('a', href=True):
                href = a.get('href', '')
                if '/series/' not in href.lower() or 'core' not in href.lower():
                    continue
                # Filtrar solo series recientes
                for keyword in self.SERIES_KEYWORDS:
                    if keyword in href.lower():
                        url_completa = href if href.startswith('http') else f"https://ark.intel.com{href}"
                        if url_completa not in [s[1] for s in series_urls]:
                            texto = a.text.strip() or keyword
                            series_urls.append((texto, url_completa))
                        break

            print(f"  [INTEL] {len(series_urls)} series de procesadores encontradas.")

            if not series_urls:
                print("  [INTEL] Sin series encontradas. Intentando paginas directas...")
                # Fallback: intentar con la pagina de productos Core directamente
                self._scrapearPaginaDirecta(driver)
                return

            totalGuardados = 0
            for nombre_serie, url_serie in series_urls[:6]:
                try:
                    guardados = self._scrapearSerie(driver, nombre_serie, url_serie)
                    totalGuardados += guardados
                    self._esperar(1, 2)
                except Exception as e:
                    print(f"  [INTEL] Error en serie {nombre_serie[:40]}: {e}")

            print(f"  [INTEL] Extraccion completada: {totalGuardados} CPUs guardados.")

        finally:
            driver.quit()

    def _scrapearSerie(self, driver, nombre_serie, url_serie):
        """Navega a una serie de procesadores ARK y extrae la tabla de productos."""
        print(f"  [INTEL]   -> Serie: {nombre_serie[:60]}")
        driver.get(url_serie)
        time.sleep(6)

        sopa = BeautifulSoup(driver.page_source, 'html.parser')

        # ARK muestra una tabla con columnas: Product Name, Launch Date, Total Cores, Max Turbo, Cache, GPU
        tablas = sopa.find_all('table')
        if not tablas:
            print(f"  [INTEL]   Sin tablas en {nombre_serie[:40]}")
            return 0

        guardados = 0
        for tabla in tablas:
            rows = tabla.find_all('tr')
            for row in rows[:20]:
                celdas = row.find_all('td')
                if len(celdas) < 4:
                    continue

                try:
                    nombre = celdas[0].text.strip()
                    # Filtrar solo procesadores Core / Core Ultra
                    if 'Core' not in nombre and 'core' not in nombre.lower():
                        continue

                    modelo = nombre if 'Intel' in nombre else f"Intel {nombre}"
                    # Limpiar caracteres especiales Unicode
                    modelo = modelo.replace('\u00ae', '').replace('\u2122', '').strip()
                    modelo = ' '.join(modelo.split())

                    # Total Cores (columna 2)
                    nucleos_text = celdas[2].text.strip()
                    nucleos = self._extraerNumero(nucleos_text, r'(\d+)') or 4

                    # Max Turbo Frequency (columna 3)
                    turbo_text = celdas[3].text.strip()
                    frecTurbo = self._extraerDecimal(turbo_text, r'(\d+[.,]\d+)') or 4.0
                    frecBase = round(frecTurbo * 0.7, 1)  # Estimar base como ~70% del turbo

                    # Estimar hilos y TDP
                    hilos = nucleos * 2 if nucleos <= 8 else nucleos + (nucleos // 2)
                    tdp = self._estimarTDP(nombre, nucleos)

                    # URL del SKU
                    enlace = celdas[0].find('a')
                    urlCpu = url_serie
                    if enlace and enlace.get('href', '').startswith('/'):
                        urlCpu = f"https://ark.intel.com{enlace['href']}"

                    self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecTurbo, tdp, urlCpu)
                    print(f"  [INTEL]   Guardado: {modelo[:55]} | {nucleos}C | Turbo:{frecTurbo}GHz")
                    guardados += 1

                except Exception as e:
                    print(f"  [INTEL]   Error procesando fila: {e}")

        return guardados

    def _scrapearPaginaDirecta(self, driver):
        """Fallback: intenta extraer SKUs de la pagina de productos Core directamente."""
        url = "https://www.intel.com/content/www/us/en/products/details/processors/core.html"
        print(f"  [INTEL] Intentando pagina directa: {url}")
        driver.get(url)
        time.sleep(6)

        sopa = BeautifulSoup(driver.page_source, 'html.parser')
        sku_links = []
        for a in sopa.find_all('a', href=True):
            href = a.get('href', '')
            if '/sku/' in href:
                url_completa = href if href.startswith('http') else f"https://www.intel.com{href}"
                if url_completa not in sku_links:
                    sku_links.append(url_completa)

        print(f"  [INTEL] {len(sku_links)} SKUs encontrados en pagina directa.")

        guardados = 0
        for sku_url in sku_links[:15]:
            try:
                # Extraer nombre del modelo de la URL
                match = re.search(r'/sku/\d+/(.+?)/specifications', sku_url)
                if not match:
                    continue
                nombre_raw = match.group(1).replace('-', ' ').title()
                modelo = nombre_raw.replace('Intel ', 'Intel ')

                # Extraer frecuencia de la URL
                freq_match = re.search(r'up-to-(\d+)-(\d+)-ghz', sku_url)
                frecTurbo = float(f"{freq_match.group(1)}.{freq_match.group(2)}") if freq_match else 4.0
                frecBase = round(frecTurbo * 0.7, 1)

                # Extraer cache (proxy para estimar nucleos)
                cache_match = re.search(r'(\d+)m-cache', sku_url)
                cache_mb = int(cache_match.group(1)) if cache_match else 12
                nucleos = max(4, cache_mb // 3)
                hilos = nucleos * 2
                tdp = 65

                self.dao.upsertCPU(modelo, nucleos, hilos, frecBase, frecTurbo, tdp, sku_url)
                print(f"  [INTEL] Guardado (directo): {modelo[:55]}")
                guardados += 1

            except Exception as e:
                print(f"  [INTEL] Error en SKU: {e}")

        print(f"  [INTEL] Total guardados desde pagina directa: {guardados}")

    def _estimarTDP(self, nombre, nucleos):
        """Estima el TDP basado en el tipo de procesador."""
        nombre_lower = nombre.lower()
        if 'hx' in nombre_lower:
            return 55
        elif 'h' in nombre_lower and ('13' in nombre_lower or '14' in nombre_lower or '12' in nombre_lower):
            return 45
        elif 'u' in nombre_lower or 'p' in nombre_lower:
            return 28 if nucleos >= 10 else 15
        else:
            return 65

    def _extraerNumero(self, texto, patron):
        m = re.search(patron, texto, re.IGNORECASE)
        return int(m.group(1)) if m else None

    def _extraerDecimal(self, texto, patron):
        m = re.search(patron, texto, re.IGNORECASE)
        return float(m.group(1).replace(',', '.')) if m else None
