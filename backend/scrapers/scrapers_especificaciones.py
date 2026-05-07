import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import requests
from bs4 import BeautifulSoup
from scrapers.scraper_base import ScraperBase


class MercadoLibreScraper(ScraperBase):
    """Scraper de precios y specs básicas desde MercadoLibre Argentina."""

    TIENDA = "Mercado Libre"

    def ejecutarScraping(self):
        url = f"https://listado.mercadolibre.com.ar/computacion/laptops-accesorios/notebooks/{self.marca.lower()}"
        print(f"  [ML] Buscando '{self.marca}' en {url}")

        driver = self._crearDriver()
        try:
            driver.get(url)
            print("  [ML] Esperando renderizado de seguridad...")
            time.sleep(5)

            sopa = BeautifulSoup(driver.page_source, 'lxml')
            items = sopa.find_all('li', class_='ui-search-layout__item')
            print(f"  [ML] {len(items)} productos encontrados.")

            if not items:
                print("  [ML] Sin resultados. ML puede haber cambiado la estructura HTML.")
                return

            for item in items[:10]:
                try:
                    titulo_tag = item.find('h2') or item.find('h3')
                    if not titulo_tag:
                        continue
                    modelo = titulo_tag.text.strip()

                    precio_tag = item.find('span', class_='andes-money-amount__fraction')
                    if not precio_tag:
                        continue
                    precio = float(precio_tag.text.replace('.', '').replace(',', '.'))

                    enlace_tag = item.find('a')
                    urlVenta = enlace_tag['href'] if enlace_tag else ""

                    # Imagen del producto (ML usa data-src para lazy loading)
                    img_tag = item.find('img', class_='ui-search-result-image__element') or item.find('img')
                    imgUrl = ""
                    if img_tag:
                        imgUrl = img_tag.get('data-src') or img_tag.get('src', '')
                        if not imgUrl.startswith('http'):
                            imgUrl = ""

                    specs = self.extraerSpecsDeTexto(modelo)
                    self.dao.upsertLaptop(
                        modelo, imgUrl, self.marca,
                        1.8, 15.6,
                        144 if "gamer" in modelo.lower() else 60,
                        50,
                        specs["cpuModelo"], specs["gpuModelo"],
                        specs["ramGb"], specs["almacenamientoGb"],
                        precio, urlVenta, self.TIENDA
                    )
                    print(f"  [ML] Guardado: {modelo[:60]} — ${precio}")
                    self._esperar(0.5, 1.5)

                except Exception as e:
                    print(f"  [ML] Error en producto: {e}")

        finally:
            driver.quit()


class CompraGamerScraper(ScraperBase):
    """Scraper de precios desde Compra Gamer (compragamer.com)."""

    TIENDA = "Compra Gamer"
    # URL del listado de notebooks en Compra Gamer
    URL_BASE = "https://www.compragamer.com/?categoria=5"

    def ejecutarScraping(self):
        print(f"  [CG] Buscando '{self.marca}' en Compra Gamer...")

        driver = self._crearDriver()
        try:
            driver.get(self.URL_BASE)
            print("  [CG] Esperando carga del sitio...")
            time.sleep(4)

            sopa = BeautifulSoup(driver.page_source, 'lxml')

            # Compra Gamer lista productos en elementos con clase 'contenedorPublicacion'
            items = sopa.find_all('div', class_='contenedorPublicacion')

            if not items:
                # Fallback: intentar con clases alternativas que Compra Gamer suele usar
                items = sopa.find_all('div', class_=lambda c: c and 'producto' in c.lower())

            print(f"  [CG] {len(items)} productos encontrados.")

            if not items:
                print("  [CG] Sin resultados. Compra Gamer puede haber cambiado la estructura HTML.")
                return

            for item in items[:10]:
                try:
                    # Nombre del producto
                    nombre_tag = (
                        item.find('p', class_='nombre') or
                        item.find('h3') or
                        item.find('span', class_='nombreProducto')
                    )
                    if not nombre_tag:
                        continue
                    modelo = nombre_tag.text.strip()

                    # Filtrar por marca deseada
                    if self.marca.lower() not in modelo.lower():
                        continue

                    # Precio
                    precio_tag = (
                        item.find('p', class_='precio') or
                        item.find('span', class_='precio') or
                        item.find('div', class_='precio')
                    )
                    if not precio_tag:
                        continue
                    precioTexto = precio_tag.text.strip().replace('$', '').replace('.', '').replace(',', '.').strip()
                    precio = float(''.join(c for c in precioTexto if c.isdigit() or c == '.'))

                    # URL del producto
                    enlace_tag = item.find('a')
                    urlVenta = f"https://www.compragamer.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else (enlace_tag['href'] if enlace_tag else "")

                    specs = self.extraerSpecsDeTexto(modelo)
                    self.dao.upsertLaptop(
                        modelo, "", self.marca,
                        1.8, 15.6,
                        144 if "gamer" in modelo.lower() else 60,
                        50,
                        specs["cpuModelo"], specs["gpuModelo"],
                        specs["ramGb"], specs["almacenamientoGb"],
                        precio, urlVenta, self.TIENDA
                    )
                    print(f"  [CG] Guardado: {modelo[:60]} — ${precio}")
                    self._esperar(0.5, 1.5)

                except Exception as e:
                    print(f"  [CG] Error en producto: {e}")

        finally:
            driver.quit()
