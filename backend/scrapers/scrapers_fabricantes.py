import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapers.scraper_base import ScraperBase


class AsusScraperLaptops(ScraperBase):
    """
    Scraper de ESPECIFICACIONES — ASUS Argentina (sitio oficial).
    Rol: extraer specs tecnicas reales (CPU, RAM, GPU, pantalla, peso, bateria).
    NO extrae precios (ASUS redirige a retailers). Guarda precio=0.

    Estrategia:
    1. Navegar al catalogo all-products con Selenium
    2. Scrollear para cargar lazy loading
    3. Extraer links a paginas de detalle de cada laptop
    4. Visitar cada detalle y extraer specs de las tablas de especificaciones
    """

    URL_CATALOGO = "https://www.asus.com/ar/laptops/all-products/"

    def __init__(self):
        super().__init__("Asus")

    def ejecutarScraping(self):
        print(f"  [ASUS] Accediendo al catalogo oficial: {self.URL_CATALOGO}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL_CATALOGO)
            print("  [ASUS] Esperando renderizado JS + scrolleando...")
            self._scrollParaCargar(driver)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')

            # Estrategia multi-selector para encontrar product cards
            items = self._buscarProductCards(sopa)

            print(f"  [ASUS] {len(items)} productos encontrados en el catalogo.")
            if not items:
                print("  [ASUS] Sin resultados con selectores de cards.")
                print("  [ASUS] Intentando extraccion alternativa por enlaces...")
                items = self._extraerPorEnlaces(sopa)
                if not items:
                    return

            productosExtraidos = 0
            for item in items[:15]:
                try:
                    resultado = self._extraerDatosDeCard(item, driver)
                    if resultado:
                        productosExtraidos += 1
                except Exception as e:
                    print(f"  [ASUS] Error procesando producto: {e}")

            print(f"  [ASUS] Extraccion completada: {productosExtraidos} productos guardados.")

        finally:
            driver.quit()

    def _scrollParaCargar(self, driver):
        """Scrollea la pagina progresivamente para activar lazy loading."""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)
            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {(i + 1) * 1500});")
                time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        except Exception as e:
            print(f"  [ASUS] Error durante scroll: {e}")

    def _buscarProductCards(self, sopa):
        """Intenta multiples selectores CSS para encontrar tarjetas de producto."""
        selectores = [
            ('div', {'class_': lambda c: c and 'ProductCard' in c}),
            ('div', {'class_': lambda c: c and isinstance(c, str) and 'product-card' in c}),
            ('div', {'class_': lambda c: c and isinstance(c, str) and 'product' in c.lower() and 'card' in c.lower()}),
            ('a', {'class_': lambda c: c and isinstance(c, str) and 'product' in c.lower()}),
            ('div', {'class_': lambda c: c and isinstance(c, str) and 'card__wrapper' in c.lower()}),
        ]
        for tag, attrs in selectores:
            items = sopa.find_all(tag, **attrs)
            if items:
                print(f"  [ASUS] Cards encontradas con selector: <{tag}> ({len(items)} items)")
                return items
        return []

    def _extraerPorEnlaces(self, sopa):
        """Fallback: buscar todos los enlaces a paginas individuales de laptops."""
        enlaces = sopa.find_all('a', href=lambda h: h and '/ar/laptops/' in h and h.count('/') >= 5)
        vistos = set()
        items_unicos = []
        for a in enlaces:
            href = a.get('href', '')
            if href not in vistos and '/filter' not in href and '/all-' not in href:
                vistos.add(href)
                items_unicos.append(a)
        print(f"  [ASUS] {len(items_unicos)} enlaces unicos a productos encontrados.")
        return items_unicos

    def _extraerDatosDeCard(self, item, driver):
        """Extrae nombre, imagen y link de un card. Visita detalle para specs reales."""
        nombre_tag = (
            item.find('h3') or item.find('h2') or item.find('h4') or
            item.find('span', class_=lambda c: c and isinstance(c, str) and 'name' in c.lower()) or
            item.find('p', class_=lambda c: c and isinstance(c, str) and 'name' in c.lower())
        )
        nombre = ""
        if nombre_tag:
            nombre = nombre_tag.text.strip()
        elif item.name == 'a':
            nombre = item.text.strip().split('\n')[0].strip()

        if not nombre or len(nombre) < 3:
            return False

        modelo = f"ASUS {nombre}" if "asus" not in nombre.lower() else nombre

        # Extraer link a detalle
        enlace_tag = item.find('a') if item.name != 'a' else item
        urlDetalle = ""
        if enlace_tag and enlace_tag.get('href', '').startswith('/'):
            urlDetalle = f"https://www.asus.com{enlace_tag['href']}"
        elif enlace_tag and enlace_tag.get('href', '').startswith('http'):
            urlDetalle = enlace_tag['href']

        # Extraer imagen del card
        img_tag = item.find('img')
        imgUrl = ""
        if img_tag:
            imgUrl = img_tag.get('data-src') or img_tag.get('src') or img_tag.get('data-lazy-src', '')
            if not imgUrl.startswith('http'):
                imgUrl = ""

        # Visitar pagina de detalle para extraer specs REALES
        specs = self._extraerSpecsDeDetalle(driver, urlDetalle) if urlDetalle else None

        if not specs:
            # Fallback: extraer lo que se pueda del texto del card (no inventar valores)
            texto_card = item.get_text(separator=" ")
            specs = self.extraerSpecsDeTexto(texto_card)
            specs["pesoKg"] = 0
            specs["tamanioPantalla"] = 0
            specs["tasaRefrescoHz"] = 0
            specs["capacidadBateriaWh"] = 0

        self.dao.upsertLaptop(
            modelo, imgUrl, self.marca,
            specs.get("pesoKg", 0), specs.get("tamanioPantalla", 0),
            specs.get("tasaRefrescoHz", 0), specs.get("capacidadBateriaWh", 0),
            specs["cpuModelo"], specs["gpuModelo"],
            specs["ramGb"], specs["almacenamientoGb"],
            0, urlDetalle, "Asus Oficial"
        )
        print(f"  [ASUS] Guardado: {modelo[:60]} | CPU: {specs['cpuModelo']} | RAM: {specs['ramGb']}GB")
        self._esperar(1, 2.5)
        return True

    def _extraerSpecsDeDetalle(self, driver, url):
        """Navega a la pagina de detalle y extrae specs de la tabla de especificaciones."""
        if not url:
            return None
        try:
            print(f"  [ASUS]   -> Visitando detalle: {url[:80]}...")
            driver.get(url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 2000);")
            time.sleep(2)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            texto_completo = sopa.get_text(separator=" ").lower()

            specs = {
                "cpuModelo": "Desconocido", "gpuModelo": "Integrada",
                "ramGb": 8, "almacenamientoGb": 256,
                "pesoKg": 0, "tamanioPantalla": 0,
                "tasaRefrescoHz": 0, "capacidadBateriaWh": 0
            }

            # Buscar en tablas/divs de specs
            spec_sections = (
                sopa.find_all('div', class_=lambda c: c and isinstance(c, str) and 'spec' in c.lower()) or
                sopa.find_all('table') or
                sopa.find_all('dl')
            )
            for seccion in spec_sections:
                texto_completo += " " + seccion.get_text(separator=" ").lower()

            # Extraer cada spec con regex robusto
            self._parsearSpecsDeTexto(specs, texto_completo)
            return specs

        except Exception as e:
            print(f"  [ASUS]   -> Error extrayendo specs de detalle: {e}")
            return None

class LenovoScraperLaptops(ScraperBase):
    """
    Scraper de ESPECIFICACIONES — Lenovo (PSREF + sitio oficial AR).
    Rol: extraer specs tecnicas reales (CPU, RAM, GPU, pantalla, peso, bateria).
    NO extrae precios. Guarda precio=0.

    Estrategia:
    1. Fuente primaria: PSREF (psref.lenovo.com) — datos estructurados y estables
    2. Fallback: sitio consumidor de Lenovo AR
    """

    URL_PSREF = "https://psref.lenovo.com/Product/Lenovo"
    URL_CONSUMER = "https://www.lenovo.com/ar/es/laptops/"

    def __init__(self):
        super().__init__("Lenovo")

    def ejecutarScraping(self):
        print(f"  [LENOVO] Intentando extraccion desde PSREF...")
        driver = self._crearDriver()
        try:
            exito = self._scrapearPSREF(driver)
            if not exito:
                print("  [LENOVO] PSREF no dio resultados. Intentando sitio consumidor...")
                self._scrapearSitioConsumidor(driver)
        finally:
            driver.quit()

    def _scrapearPSREF(self, driver):
        """Extrae specs desde PSREF (Product Specifications Reference de Lenovo)."""
        try:
            driver.get(self.URL_PSREF)
            print("  [LENOVO] Esperando carga de PSREF...")
            time.sleep(5)

            for i in range(3):
                driver.execute_script(f"window.scrollTo(0, {(i + 1) * 1000});")
                time.sleep(1)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')

            # PSREF lista productos como enlaces — URLs usan /l/Product/ con submarca
            enlaces_producto = []
            # Submarcas de laptops Lenovo (excluimos monitores, desktops, AIO)
            submarcas_laptop = ['ideapad', 'thinkpad', 'yoga', 'legion', 'v15', 'v14',
                                'thinkbook', 'loq', 'flex', 'slim', 'e14', 'e16', 'l14',
                                'l16', 'p16', 't14', 'x13', 'x1']
            for a in sopa.find_all('a', href=True):
                href = a.get('href', '')
                texto = a.text.strip()
                # Aceptar tanto /Product/ como /l/Product/
                if ('/Product/' in href or '/l/Product/' in href) and len(texto) > 5:
                    # Filtrar monitores, desktops, AIO, accesorios
                    texto_lower = texto.lower()
                    href_lower = href.lower()
                    if any(excl in texto_lower or excl in href_lower for excl in ['monitor', 'desktop', 'aio', 'tower', 'thinkcentre', 'thinkvision', 'thinksmart']):
                        continue
                    if any(k in texto_lower or k in href_lower for k in submarcas_laptop):
                        url_completa = href if href.startswith('http') else f"https://psref.lenovo.com{href}"
                        enlaces_producto.append((texto, url_completa))

            # Deduplicar
            vistos = set()
            enlaces_unicos = []
            for nombre, url in enlaces_producto:
                if url not in vistos:
                    vistos.add(url)
                    enlaces_unicos.append((nombre, url))

            print(f"  [LENOVO] {len(enlaces_unicos)} productos encontrados en PSREF.")
            if not enlaces_unicos:
                return False

            productosGuardados = 0
            for nombre, url in enlaces_unicos[:15]:
                try:
                    specs = self._extraerSpecsDePSREF(driver, url)
                    if specs:
                        nombre_limpio = nombre.strip()
                        if nombre_limpio.lower() in ['view details', 'details', 'ver detalles', 'ver detalle', 'specs', 'specifications', 'click here', '']:
                            # Extraer de la URL, e.g., https://psref.lenovo.com/Product/ThinkPad/ThinkPad_E14_Gen_8_AMD -> ThinkPad E14 Gen 8 AMD
                            parts = [p for p in url.split('/') if p]
                            if parts:
                                nombre_limpio = parts[-1].replace('_', ' ')
                        
                        modelo = nombre_limpio if "lenovo" in nombre_limpio.lower() else f"Lenovo {nombre_limpio}"
                        self.dao.upsertLaptop(
                            modelo, specs.get("imgUrl", ""), self.marca,
                            specs.get("pesoKg", 0), specs.get("tamanioPantalla", 0),
                            specs.get("tasaRefrescoHz", 0), specs.get("capacidadBateriaWh", 0),
                            specs["cpuModelo"], specs["gpuModelo"],
                            specs["ramGb"], specs["almacenamientoGb"],
                            0, url, "Lenovo Oficial"
                        )
                        print(f"  [LENOVO] Guardado: {modelo[:60]} | CPU: {specs['cpuModelo']} | RAM: {specs['ramGb']}GB")
                        productosGuardados += 1
                        self._esperar(1, 2.5)
                except Exception as e:
                    print(f"  [LENOVO] Error procesando {nombre[:40]}: {e}")

            print(f"  [LENOVO] PSREF completado: {productosGuardados} productos guardados.")
            return productosGuardados > 0

        except Exception as e:
            print(f"  [LENOVO] Error en PSREF: {e}")
            return False

    def _extraerSpecsDePSREF(self, driver, url):
        """Extrae specs detalladas de una pagina individual de PSREF."""
        try:
            driver.get(url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 1500);")
            time.sleep(2)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            texto = sopa.get_text(separator=" ").lower()

            specs = {
                "cpuModelo": "Desconocido", "gpuModelo": "Integrada",
                "ramGb": 8, "almacenamientoGb": 256,
                "pesoKg": 0, "tamanioPantalla": 0,
                "tasaRefrescoHz": 0, "capacidadBateriaWh": 0,
                "imgUrl": ""
            }

            # Imagen del producto
            img_tag = sopa.find('img', class_=lambda c: c and isinstance(c, str) and 'product' in c.lower())
            if not img_tag:
                img_tag = sopa.find('img', src=lambda s: s and 'Product' in s if s else False)
            if img_tag:
                img_src = img_tag.get('src', '') or img_tag.get('data-src', '')
                if img_src.startswith('http'):
                    specs["imgUrl"] = img_src
                elif img_src.startswith('/'):
                    specs["imgUrl"] = f"https://psref.lenovo.com{img_src}"

            # Parsear specs del texto
            self._parsearSpecsDeTexto(specs, texto)
            return specs

        except Exception as e:
            print(f"  [LENOVO]   -> Error extrayendo specs de PSREF: {e}")
            return None

    def _scrapearSitioConsumidor(self, driver):
        """Fallback: extrae datos desde el sitio consumidor de Lenovo AR."""
        try:
            driver.get(self.URL_CONSUMER)
            print("  [LENOVO] Esperando renderizado JS del sitio consumidor...")
            time.sleep(6)

            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {(i + 1) * 1500});")
                time.sleep(1.5)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')

            items = (
                sopa.find_all('div', class_=lambda c: c and isinstance(c, str) and 'product-card' in c) or
                sopa.find_all('div', class_=lambda c: c and isinstance(c, str) and 'product' in c.lower() and 'card' in c.lower()) or
                sopa.find_all('article', class_=lambda c: c and isinstance(c, str) and 'product' in c.lower()) or
                sopa.find_all('div', attrs={'data-product-id': True})
            )

            print(f"  [LENOVO] {len(items)} productos en sitio consumidor.")
            if not items:
                print("  [LENOVO] Sin productos en sitio consumidor.")
                return

            for item in items[:10]:
                try:
                    nombre_tag = (
                        item.find('h3') or item.find('h2') or
                        item.find('div', class_=lambda c: c and isinstance(c, str) and 'title' in c.lower()) or
                        item.find('a', class_=lambda c: c and isinstance(c, str) and 'title' in c.lower())
                    )
                    if not nombre_tag:
                        continue
                    modelo = nombre_tag.text.strip()
                    if "lenovo" not in modelo.lower():
                        modelo = f"Lenovo {modelo}"

                    specs_texto = item.get_text(separator=" ")
                    specs = self.extraerSpecsDeTexto(specs_texto)

                    enlace_tag = item.find('a')
                    urlProducto = ""
                    if enlace_tag and enlace_tag.get('href', '').startswith('/'):
                        urlProducto = f"https://www.lenovo.com{enlace_tag['href']}"
                    elif enlace_tag and enlace_tag.get('href', '').startswith('http'):
                        urlProducto = enlace_tag['href']

                    img_tag = item.find('img')
                    imgUrl = ""
                    if img_tag:
                        imgUrl = img_tag.get('data-src') or img_tag.get('src', '')
                        if not imgUrl.startswith('http'):
                            imgUrl = ""

                    # Guardar con specs del texto visible — sin inventar valores
                    self.dao.upsertLaptop(
                        modelo, imgUrl, self.marca,
                        0, 0, 0, 0,
                        specs["cpuModelo"], specs["gpuModelo"],
                        specs["ramGb"], specs["almacenamientoGb"],
                        0, urlProducto, "Lenovo Oficial"
                    )
                    print(f"  [LENOVO] Guardado (consumidor): {modelo[:60]}")
                    self._esperar()

                except Exception as e:
                    print(f"  [LENOVO] Error en producto: {e}")

        except Exception as e:
            print(f"  [LENOVO] Error en sitio consumidor: {e}")
