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
from utils.normalizacion import validar_url_retail


class MercadoLibreScraper(ScraperBase):
    """
    Scraper de RETAILERS — MercadoLibre Argentina.
    Rol: extraer SOLO precio, link de compra e imagen de referencia.
    NO extrae especificaciones técnicas (eso lo hacen los scrapers de fabricantes).
    """

    TIENDA = "Mercado Libre"

    # Palabras clave que confirman que es una laptop (si estan presentes, ignoramos exclusiones ambiguas)
    KEYWORDS_LAPTOP = ['notebook', 'laptop', 'ultrabook', 'netbook', 'portatil']

    # Exclusiones fuertes: estos NUNCA son laptops
    EXCLUSIONES_FUERTES = r'\b(tablet|tablets|ipad|ipads|funda|fundas|soporte|soportes|cargador|cargadores|repuesto|repuestos|caja|cajas|bolso|bolsos|mochila|mochilas|vidrio|vidrios|protector|protectores|mouse|cable|cables|lapiz|lapices|auricular|auriculares|cooler|hub|docking|disco\s+externo)\b'

    # Exclusiones ambiguas: solo se aplican si NO hay keywords de laptop en el titulo
    EXCLUSIONES_AMBIGUAS = r'\b(teclado|teclados|pantalla|pantallas|bateria|baterias|memoria\s+ram|modulo)\b'

    RUTAS_ML = {
        'CPU': 'computacion/componentes-pc/procesadores',
        'GPU': 'computacion/componentes-pc/placas-video',
        'RAM': 'computacion/componentes-pc/memorias-ram',
        'Laptop': 'computacion/laptops-accesorios/notebooks',
        'Almacenamiento': 'computacion/componentes-pc/discos-accesorios',
    }

    def __init__(self, marca, categoria="Laptop"):
        super().__init__(marca)
        self.categoria = categoria

    def ejecutarScraping(self):
        ruta = self.RUTAS_ML.get(self.categoria, 'computacion')
        url = f"https://listado.mercadolibre.com.ar/{ruta}/{self.marca.lower()}"
        print(f"  [ML] Buscando '{self.marca}' en {url}")

        driver = self._crearDriver()
        try:
            driver.get(url)
            print("  [ML] Esperando renderizado de seguridad...")
            time.sleep(5)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            items = sopa.find_all('li', class_='ui-search-layout__item')
            print(f"  [ML] {len(items)} productos encontrados.")

            if not items:
                print("  [ML] Sin resultados. ML puede haber cambiado la estructura HTML.")
                return

            guardados = 0
            for item in items[:15]:
                try:
                    titulo_tag = item.find('h2') or item.find('h3')
                    if not titulo_tag:
                        continue
                    modelo = titulo_tag.text.strip()
                    modelo_lower = modelo.lower()

                    # Safety check: skip used items
                    if "usado" in item.text.lower():
                        print(f"  [ML] Filtrado (producto usado): {modelo[:60]}")
                        continue

                    # Exclusiones fuertes: siempre se filtran
                    if re.search(self.EXCLUSIONES_FUERTES, modelo_lower):
                        print(f"  [ML] Filtrado (accesorio): {modelo[:60]}")
                        continue

                    # Exclusiones específicas por categoría
                    if self.categoria == "Laptop":
                        es_laptop = any(kw in modelo_lower for kw in self.KEYWORDS_LAPTOP)
                        if not es_laptop and re.search(self.EXCLUSIONES_AMBIGUAS, modelo_lower):
                            print(f"  [ML] Filtrado (probablemente repuesto): {modelo[:60]}")
                            continue

                    precio_tag = item.find('span', class_='andes-money-amount__fraction')
                    if not precio_tag:
                        continue
                    precio = float(precio_tag.text.replace('.', '').replace(',', '.'))

                    enlace_tag = item.find('a')
                    urlVenta = enlace_tag['href'] if enlace_tag else ""
                    if urlVenta and '?' in urlVenta:
                        urlVenta = urlVenta.split('?')[0]

                    # Safety check: skip invalid URLs (sponsored ads, etc.)
                    if not validar_url_retail(urlVenta, self.TIENDA):
                        print(f"  [ML] Enlace descartado por invalido: {urlVenta}")
                        continue

                    # Imagen del producto (ML usa data-src para lazy loading)
                    img_tag = item.find('img', class_='ui-search-result-image__element') or item.find('img')
                    imgUrl = ""
                    if img_tag:
                        imgUrl = img_tag.get('data-src') or img_tag.get('src', '')
                        if not imgUrl.startswith('http'):
                            imgUrl = ""

                    # Solo guardamos precio, link e imagen — SIN specs técnicas
                    self.dao.upsertProductoRetail(
                        modelo, imgUrl, self.marca,
                        self.categoria,
                        precio, urlVenta, self.TIENDA
                    )
                    print(f"  [ML] Guardado: {modelo[:60]} — ${precio}")
                    guardados += 1
                    self._esperar(0.5, 1.5)

                except Exception as e:
                    print(f"  [ML] Error en producto: {e}")

            print(f"  [ML] Total guardados: {guardados}")

        finally:
            driver.quit()


class CompraGamerScraper(ScraperBase):
    """
    Scraper de RETAILERS — Compra Gamer (compragamer.com).
    Sitio Angular 18: usa WebDriverWait para esperar el renderizado real
    antes de parsear. Soporta categorías Laptop, CPU, GPU, RAM y Almacenamiento.
    """

    TIENDA = "Compra Gamer"
    BASE_URL = "https://www.compragamer.com"

    # IDs reales del parámetro ?cate= en CompraGamer (verificados 21/05/2026)
    CATEGORIAS_URL = {
        "Laptop":          58,
        "CPU_AMD":         27,
        "CPU_Intel":       48,
        "GPU":              6,
        "RAM":             15,
        "Almacenamiento":  81,
    }

    # Accesorios y periféricos que nunca son el producto que buscamos
    EXCLUSIONES = [
        'mouse', 'teclado', 'auricular', 'monitor', 'webcam',
        'mochila', 'funda', 'silla', 'pad', 'headset', 'joystick',
        'parlante', 'ups', 'cámara', 'camara', 'impresora', 'soporte',
    ]

    def __init__(self, marca, categoria="Laptop"):
        super().__init__(marca)
        self.categoria = categoria

    def _resolverCategoriaId(self):
        """CPUs AMD e Intel tienen páginas separadas en CompraGamer."""
        if self.categoria == "CPU":
            return self.CATEGORIAS_URL.get(
                "CPU_Intel" if self.marca.lower() == "intel" else "CPU_AMD"
            )
        return self.CATEGORIAS_URL.get(self.categoria)

    def ejecutarScraping(self):
        idCategoria = self._resolverCategoriaId()
        if not idCategoria:
            print(f"  [CG] Categoria '{self.categoria}' no soportada.")
            return

        url = f"{self.BASE_URL}/productos?cate={idCategoria}"
        print(f"  [CG] [{self.categoria}] Buscando '{self.marca}' -> {url}")

        driver = self._crearDriver()
        try:
            driver.get(url)
            self._esperarRenderizado(driver)
            self._scrollParaCargar(driver)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            items = self._extraerCards(sopa)

            print(f"  [CG] {len(items)} tarjetas encontradas.")
            if not items:
                print("  [CG] Sin resultados — Angular puede no haber terminado de renderizar.")
                return

            guardados = 0
            for item in items[:20]:
                try:
                    if self._procesarItem(item):
                        guardados += 1
                        self._esperar(0.5, 1.5)
                except Exception as e:
                    print(f"  [CG] Error procesando tarjeta: {e}")

            print(f"  [CG] Total guardados: {guardados}")

        finally:
            driver.quit()

    # ── Helpers privados ────────────────────────────────────────────────────

    def _esperarRenderizado(self, driver):
        """
        Espera a que Angular 18 termine de cargar los productos.
        Estrategia 1: esperar el componente cgw-product-card en el DOM.
        Estrategia 2: esperar estabilidad de Angular via getAllAngularTestabilities().
        Estrategia 3: sleep fijo como último recurso.
        """
        print("  [CG] Esperando renderizado Angular...")

        # Estrategia 1 — componente Angular o clase CSS de tarjeta
        try:
            WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                    "cgw-product-card, app-product-card, "
                    "a[href*='/producto/'], a[href*='/productos/']"
                ))
            )
            print("  [CG] Componentes de producto detectados en el DOM.")
            return
        except Exception:
            pass

        # Estrategia 2 — estabilidad interna de Angular
        try:
            WebDriverWait(driver, 20).until(lambda d: d.execute_script(
                "try { return window.getAllAngularTestabilities()[0].isStable(); }"
                "catch(e) { return document.readyState === 'complete'; }"
            ))
            print("  [CG] Angular reporta zona estable.")
            return
        except Exception:
            pass

        # Estrategia 3 — fallback con sleep
        print("  [CG] Timeout en detección Angular. Esperando 8s adicionales...")
        time.sleep(8)

    def _scrollParaCargar(self, driver):
        """Scrollea en pasos para disparar el lazy loading de Angular."""
        for i in range(5):
            driver.execute_script(f"window.scrollTo(0, {(i + 1) * 1800});")
            time.sleep(0.7)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

    def _extraerCards(self, sopa):
        """
        Prueba selectores en orden de especificidad decreciente.
        El sitio usa componentes Angular con prefijo cgw-,
        pero las cards también son etiquetas <a> con href de producto.
        """
        # Selector 1: componente Angular nativo
        items = sopa.find_all('cgw-product-card')
        if items:
            return items

        # Selector 2: clase CSS product-card (excluye botones del header)
        items = [
            tag for tag in sopa.find_all(class_='product-card')
            if 'product-card__button' not in ' '.join(tag.get('class', []))
        ]
        if items:
            return items

        # Selector 3: enlaces directos a páginas de producto
        items = sopa.find_all('a', href=lambda h: h and (
            '/producto/' in h or '/productos/' in h
        ))
        if items:
            return items

        return []

    def _procesarItem(self, item):
        """Extrae datos de una tarjeta y persiste en BD. Retorna True si guardó."""

        # ── Nombre ───────────────────────────────────────────────────────────
        nombre_tag = (
            item.find(class_='product-card__title') or
            item.find(class_='product-card__name')  or
            item.find('h3') or
            item.find('h2') or
            item.find('p', class_='nombre')
        )
        if not nombre_tag:
            return False

        modelo = nombre_tag.get_text(strip=True)
        modelo_lower = modelo.lower()

        # ── Filtros ──────────────────────────────────────────────────────────
        aliases = {
            'intel': ['intel', 'core i3', 'core i5', 'core i7', 'core i9', 'core ultra'],
            'nvidia': ['nvidia', 'geforce', 'rtx', 'gtx'],
            'kingston': ['kingston', 'fury', 'hyperx'],
            'amd': ['amd', 'radeon', 'rx '],
            'western digital': ['western digital', 'wd ', 'wd_black', 'wd_blue', 'wd_green', 'wd_red'],
            'adata': ['adata', 'xpg'],
            'corsair': ['corsair', 'vengeance'],
            'crucial': ['crucial'],
            'team': ['team', 'teamgroup', 't-force'],
            'gskill': ['g.skill', 'gskill', 'trident', 'ripjaws'],
            'patriot': ['patriot', 'viper'],
        }
        terminos = aliases.get(self.marca.lower(), [self.marca.lower()])
        if self.marca.lower() != 'todas' and not any(t in modelo_lower for t in terminos):
            return False

        if any(excl in modelo_lower for excl in self.EXCLUSIONES):
            print(f"  [CG] Filtrado (accesorio): {modelo[:60]}")
            return False

        # ── Filtros específicos por categoría ────────────────────────────────
        if self.categoria == "Laptop" and not any(
            kw in modelo_lower for kw in ['notebook', 'laptop', 'portatil']
        ):
            return False

        if self.categoria == "CPU":
            # Rechazar productos que claramente no son procesadores sueltos
            if any(kw in modelo_lower for kw in ['notebook', 'laptop', 'consola', 'pc ', 'monitor', 'mother']):
                return False
            # Requerir al menos una keyword de procesador
            if not any(kw in modelo_lower for kw in ['procesador', 'ryzen', 'core i', 'intel core', 'athlon', 'threadripper']):
                return False

        if self.categoria == "GPU":
            # Rechazar productos que no son placas de video
            if any(kw in modelo_lower for kw in ['notebook', 'laptop', 'cable', 'soporte', 'riser']):
                return False
            # Requerir keywords de GPU
            if not any(kw in modelo_lower for kw in ['geforce', 'rtx', 'gtx', 'radeon', 'rx ', 'placa de video']):
                return False

        if self.categoria == "RAM":
            # Requerir keywords de RAM
            if not any(kw in modelo_lower for kw in ['ddr4', 'ddr5', 'ddr3', 'memoria ram', 'ram ']):
                return False
            # Excluir notebooks que mencionan RAM
            if any(kw in modelo_lower for kw in ['notebook', 'laptop']):
                return False

        if self.categoria == "Almacenamiento":
            # Requerir keywords de almacenamiento
            if not any(kw in modelo_lower for kw in ['ssd', 'hdd', 'nvme', 'm.2', 'disco']):
                return False
            # Excluir gabinetes/carcasas de disco
            if any(kw in modelo_lower for kw in ['gabinete', 'carcasa', 'carry', 'case', 'adaptador']):
                return False

        # ── Precio ───────────────────────────────────────────────────────────
        precio_tag = (
            item.find(class_='txt_price') or
            item.find(class_=lambda c: c and 'price' in c.lower()
                      and 'old' not in c.lower() and 'before' not in c.lower()) or
            item.find('span', class_='precio')
        )
        if not precio_tag:
            return False

        precio_texto = re.sub(r'[^\d,.]', '', precio_tag.get_text(strip=True))
        precio_texto = precio_texto.replace('.', '').replace(',', '.')
        if not precio_texto:
            return False
        precio = float(precio_texto)
        if precio <= 0:
            return False

        # ── URL ──────────────────────────────────────────────────────────────
        urlVenta = ""
        anchor = None
        if item.name == 'a' and '/producto/' in item.get('href', ''):
            anchor = item
        else:
            anchor = item.find('a', href=lambda h: h and '/producto/' in h)
            if not anchor:
                anchor = item.find('a', href=True)
        
        if anchor and anchor.get('href'):
            href = anchor['href']
            urlVenta = f"{self.BASE_URL}{href}" if href.startswith('/') else href

        if not validar_url_retail(urlVenta, self.TIENDA):
            print(f"  [CG] Enlace descartado por invalido: {urlVenta}")
            return False

        # ── Imagen ───────────────────────────────────────────────────────────
        img_tag = item.find('img')
        imgUrl = ""
        if img_tag:
            imgUrl = img_tag.get('src') or img_tag.get('data-src', '')
            if not imgUrl.startswith('http'):
                imgUrl = ""

        # ── Determinar marca del producto para GPU/RAM/Almacenamiento ────────
        marcaProducto = self.marca
        if self.categoria == "GPU":
            # Las GPUs de CompraGamer pueden ser de múltiples fabricantes
            if any(k in modelo_lower for k in ['nvidia', 'geforce', 'rtx', 'gtx']):
                marcaProducto = "NVIDIA"
            elif any(k in modelo_lower for k in ['radeon', 'rx ']):
                marcaProducto = "AMD"

        self.dao.upsertProductoRetail(
            modelo, imgUrl, marcaProducto,
            self.categoria,
            precio, urlVenta, self.TIENDA
        )
        print(f"  [CG] Guardado: {modelo[:60]} — ${precio:,.0f}")
        return True
