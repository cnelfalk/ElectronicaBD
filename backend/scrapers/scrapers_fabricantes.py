import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from bs4 import BeautifulSoup
from scrapers.scraper_base import ScraperBase


class AsusScraperLaptops(ScraperBase):
    """
    Scraper de especificaciones desde el sitio oficial de ASUS Argentina.
    Fuente: https://www.asus.com/ar/laptops/
    No extrae precios (ASUS redirige a retailers). Guarda precio=0.
    """

    URL = "https://www.asus.com/ar/laptops/"

    def __init__(self):
        super().__init__("Asus")

    def ejecutarScraping(self):
        print(f"  [ASUS] Accediendo al catálogo oficial: {self.URL}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL)
            print("  [ASUS] Esperando renderizado JS...")
            time.sleep(5)

            sopa = BeautifulSoup(driver.page_source, 'lxml')

            # ASUS usa tarjetas de producto con clase 'ProductCard__wrapper'
            items = sopa.find_all('div', class_=lambda c: c and 'ProductCard' in c)

            if not items:
                # Fallback: buscar por estructura genérica de tarjetas
                items = sopa.find_all('div', class_=lambda c: c and 'product' in c.lower() and 'card' in c.lower())

            print(f"  [ASUS] {len(items)} productos encontrados.")
            if not items:
                print("  [ASUS] Sin resultados. ASUS puede haber cambiado su estructura HTML.")
                return

            for item in items[:10]:
                try:
                    nombre_tag = item.find('h3') or item.find('h2') or item.find('p', class_=lambda c: c and 'name' in c.lower())
                    if not nombre_tag:
                        continue
                    modelo = f"ASUS {nombre_tag.text.strip()}"

                    # Intentar obtener specs desde el texto del card
                    specs = self.extraerSpecsDeTexto(modelo)

                    # Buscar specs específicas en el card si las expone
                    specs_tags = item.find_all('li') or item.find_all('span', class_=lambda c: c and 'spec' in c.lower())
                    specs_texto = " ".join(tag.text for tag in specs_tags)
                    if specs_texto:
                        specs_extra = self.extraerSpecsDeTexto(specs_texto)
                        # Usar el valor del card si mejora el default
                        if specs_extra["cpuModelo"] != "Desconocido":
                            specs["cpuModelo"] = specs_extra["cpuModelo"]
                        if specs_extra["ramGb"] != 8:
                            specs["ramGb"] = specs_extra["ramGb"]

                    enlace_tag = item.find('a')
                    urlProducto = f"https://www.asus.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else self.URL

                    self.dao.upsertLaptop(
                        modelo, "", self.marca,
                        1.8, 15.6, 60, 50,
                        specs["cpuModelo"], specs["gpuModelo"],
                        specs["ramGb"], specs["almacenamientoGb"],
                        0, urlProducto, "Asus Oficial"
                    )
                    print(f"  [ASUS] Guardado: {modelo[:60]}")
                    self._esperar()

                except Exception as e:
                    print(f"  [ASUS] Error en producto: {e}")

        finally:
            driver.quit()


class LenovoScraperLaptops(ScraperBase):
    """
    Scraper de especificaciones desde el sitio oficial de Lenovo Argentina.
    Fuente: https://www.lenovo.com/ar/es/laptops/
    No extrae precios (Lenovo AR redirige a retailers). Guarda precio=0.
    """

    URL = "https://www.lenovo.com/ar/es/laptops/"

    def __init__(self):
        super().__init__("Lenovo")

    def ejecutarScraping(self):
        print(f"  [LENOVO] Accediendo al catálogo oficial: {self.URL}")
        driver = self._crearDriver()
        try:
            driver.get(self.URL)
            print("  [LENOVO] Esperando renderizado JS...")
            time.sleep(6)

            sopa = BeautifulSoup(driver.page_source, 'lxml')

            # Lenovo usa tarjetas con clase 'product-grid-card' o similar
            items = (
                sopa.find_all('div', class_='product-grid-card') or
                sopa.find_all('div', class_=lambda c: c and 'product' in c.lower() and 'card' in c.lower()) or
                sopa.find_all('article', class_=lambda c: c and 'product' in c.lower())
            )

            print(f"  [LENOVO] {len(items)} productos encontrados.")
            if not items:
                print("  [LENOVO] Sin resultados. Lenovo puede haber cambiado su estructura HTML.")
                return

            for item in items[:10]:
                try:
                    nombre_tag = (
                        item.find('h3') or
                        item.find('h2') or
                        item.find('div', class_=lambda c: c and 'title' in c.lower())
                    )
                    if not nombre_tag:
                        continue
                    modelo = nombre_tag.text.strip()
                    if "lenovo" not in modelo.lower():
                        modelo = f"Lenovo {modelo}"

                    specs_texto = item.get_text(separator=" ")
                    specs = self.extraerSpecsDeTexto(specs_texto)

                    enlace_tag = item.find('a')
                    urlProducto = f"https://www.lenovo.com{enlace_tag['href']}" if enlace_tag and enlace_tag.get('href', '').startswith('/') else self.URL

                    self.dao.upsertLaptop(
                        modelo, "", self.marca,
                        1.8, 15.6, 60, 50,
                        specs["cpuModelo"], specs["gpuModelo"],
                        specs["ramGb"], specs["almacenamientoGb"],
                        0, urlProducto, "Lenovo Oficial"
                    )
                    print(f"  [LENOVO] Guardado: {modelo[:60]}")
                    self._esperar()

                except Exception as e:
                    print(f"  [LENOVO] Error en producto: {e}")

        finally:
            driver.quit()
