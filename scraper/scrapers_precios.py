"""
scrapers_precios.py
-------------------
Implementaciones concretas de scrapers de PRECIOS.
Cada clase hereda de ScraperPrecios y sobreescribe `extraer()`.

La lógica fina de selectores CSS/XPath queda marcada con TODO:
se ajusta cuando inspeccionemos el HTML real de cada sitio.
"""

from .scraper_base import ScraperPrecios


class CompraGamerScraper(ScraperPrecios):
    """Scraper de precios para compragamer.com"""

    def __init__(self, id_tienda: int):
        super().__init__(
            nombre="Compra Gamer",
            url_base="https://compragamer.com",
            id_tienda=id_tienda,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de Compra Gamer...")
        resultados: list[dict] = []

        # Categorías a recorrer dentro del sitio.
        # TODO: ajustar las rutas según el sitemap real.
        categorias_url = [
            f"{self._url_base}/productos/notebooks",
            f"{self._url_base}/productos/procesadores",
            f"{self._url_base}/productos/placas-de-video",
        ]

        for url_cat in categorias_url:
            html = self._obtener_html(url_cat)
            if not html:
                continue

            soup = self._parsear(html)

            # TODO: reemplazar por los selectores reales de Compra Gamer.
            # Ejemplo tentativo (hay que inspeccionar con DevTools):
            #   tarjetas = soup.select("div.product-card")
            #   for tarjeta in tarjetas:
            #       modelo = tarjeta.select_one("h2.product-title").get_text(strip=True)
            #       precio_txt = tarjeta.select_one("span.price").get_text(strip=True)
            #       url_prod   = tarjeta.select_one("a.product-link")["href"]
            #       precio     = self._parsear_precio(precio_txt)
            #       resultados.append({
            #           "modelo": modelo,
            #           "precio": precio,
            #           "url_producto": url_prod,
            #           "id_tienda": self._id_tienda,
            #       })

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados

    @staticmethod
    def _parsear_precio(texto: str) -> float:
        """Convierte '$1.299.999,00' a 1299999.00."""
        limpio = texto.replace("$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(limpio)
        except ValueError:
            return 0.0


class MercadoLibreScraper(ScraperPrecios):
    """Scraper de precios para mercadolibre.com.ar"""

    def __init__(self, id_tienda: int):
        super().__init__(
            nombre="Mercado Libre",
            url_base="https://listado.mercadolibre.com.ar",
            id_tienda=id_tienda,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de Mercado Libre...")
        resultados: list[dict] = []

        # Términos de búsqueda
        busquedas = ["lenovo-ideapad-3", "hp-victus", "ryzen-5-4600g"]

        for termino in busquedas:
            url = f"{self._url_base}/{termino}"
            html = self._obtener_html(url)
            
            if not html:
                self._log_error(f"No se pudo obtener el HTML para {termino}")
                continue

            soup = self._parsear(html)

            # Selectores amplios
            items = soup.select("li.ui-search-layout__item, div.poly-card, div.ui-search-result")
            
            if not items:
                self._log_error(f"No se encontraron items para {termino}.")
                continue

            # Usamos un Set para guardar las URLs que ya vimos y no duplicar
            urls_vistas = set()
            agregados_termino = 0

            for item in items:
                # Si ya atrapamos 5 distintos de este término, pasamos al siguiente
                if agregados_termino >= 5:
                    break

                # Extraer título
                titulo_el = item.select_one("h2.ui-search-item__title, h2.poly-box, h2.poly-component__title, a.poly-component__title")
                if not titulo_el:
                    continue
                modelo = titulo_el.get_text(strip=True)

                # Filtro de intrusos: verificamos que la primera palabra de la búsqueda esté en el título
                # Ej: Si busco "ryzen-5-4600g", verifico que "ryzen" esté en el título.
                palabra_clave = termino.split('-')[0].lower()
                if palabra_clave not in modelo.lower():
                    continue

                # Extraer Link
                link_el = item.select_one("a.ui-search-link, a.poly-component__title")
                url_prod = link_el["href"] if link_el else ""

                # Control de duplicados por URL
                if url_prod in urls_vistas or not url_prod:
                    continue
                urls_vistas.add(url_prod)

                # Extraer precio
                precio_el = item.select_one("span.andes-money-amount__fraction, div.poly-price__current span.andes-money-amount__fraction")
                precio_txt = precio_el.get_text(strip=True) if precio_el else "0"
                precio = self._parsear_precio(precio_txt)

                resultados.append({
                    "modelo": modelo,
                    "precio": precio,
                    "url_producto": url_prod,
                    "id_tienda": self._id_tienda,
                })
                agregados_termino += 1

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados
    
    
    @staticmethod
    def _parsear_precio(texto: str) -> float:
        limpio = texto.replace(".", "").replace(",", ".").strip()
        try:
            return float(limpio)
        except ValueError:
            return 0.0
