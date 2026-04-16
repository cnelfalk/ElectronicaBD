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

        # Búsquedas por término. TODO: parametrizar desde afuera.
        busquedas = ["notebook-gamer", "procesador-amd", "procesador-intel", "placa-de-video"]

        for termino in busquedas:
            url = f"{self._url_base}/{termino}"
            html = self._obtener_html(url)
            if not html:
                continue

            soup = self._parsear(html)

            # TODO: ajustar selectores. ML cambia su HTML seguido, por eso
            # conviene centralizarlos acá para que sean fáciles de actualizar.
            # Ejemplo tentativo:
            #   items = soup.select("li.ui-search-layout__item")
            #   for item in items:
            #       modelo = item.select_one("h2.ui-search-item__title").get_text(strip=True)
            #       precio = self._parsear_precio(
            #           item.select_one("span.andes-money-amount__fraction").get_text()
            #       )
            #       url_prod = item.select_one("a.ui-search-link")["href"]
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
        limpio = texto.replace(".", "").replace(",", ".").strip()
        try:
            return float(limpio)
        except ValueError:
            return 0.0
