"""
scrapers_especificaciones.py
----------------------------
Implementaciones concretas de scrapers de ESPECIFICACIONES.
Cada uno apunta a la página oficial del fabricante.

    Componentes de escritorio -> AMD, Intel   (CPU, GPU)
    Notebooks                 -> Lenovo, Asus
"""

from .scraper_base import ScraperEspecificaciones


# =====================================================================
# COMPONENTES DE ESCRITORIO (CPU / GPU)
# =====================================================================
class AMDScraper(ScraperEspecificaciones):
    """Specs de procesadores y GPUs AMD (amd.com)."""

    def __init__(self, id_marca: int, id_categoria: int):
        super().__init__(
            nombre="AMD",
            url_base="https://www.amd.com",
            id_marca=id_marca,
            id_categoria=id_categoria,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de AMD...")
        resultados: list[dict] = []

        # TODO: definir las URLs según categoría.
        #   CPU -> https://www.amd.com/en/products/processors/desktops/ryzen.html
        #   GPU -> https://www.amd.com/en/products/graphics/desktops/radeon.html
        # Cada ficha de producto tiene una tabla de specs estructurada;
        # se parsea con BeautifulSoup y se mapea al dict de salida.

        # Estructura esperada del dict de salida (CPU):
        #   {
        #       "modelo": "Ryzen 7 7800X3D",
        #       "nucleos": 8, "hilos": 16,
        #       "frecuencia_base": 4.2, "frecuencia_turbo": 5.0,
        #       "tdp": 120, "socket": "AM5",
        #       "imagen_url": "...",
        #       "id_marca": self._id_marca,
        #       "id_categoria": self._id_categoria,
        #   }

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados


class IntelScraper(ScraperEspecificaciones):
    """Specs de procesadores Intel (ark.intel.com)."""

    def __init__(self, id_marca: int, id_categoria: int):
        super().__init__(
            nombre="Intel",
            url_base="https://ark.intel.com",
            id_marca=id_marca,
            id_categoria=id_categoria,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de Intel...")
        resultados: list[dict] = []

        # TODO: ARK tiene una API-like con filtros por familia
        # (https://ark.intel.com/content/www/us/en/ark.html#@Processors).
        # Conviene recorrer la familia Core Ultra / Core i por serie y
        # parsear las páginas de ficha individuales.

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados


# =====================================================================
# NOTEBOOKS
# =====================================================================
class LenovoScraper(ScraperEspecificaciones):
    """Specs de notebooks Lenovo (lenovo.com)."""

    def __init__(self, id_marca: int, id_categoria: int):
        super().__init__(
            nombre="Lenovo",
            url_base="https://www.lenovo.com",
            id_marca=id_marca,
            id_categoria=id_categoria,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de Lenovo...")
        resultados: list[dict] = []

        # TODO: recorrer líneas IdeaPad, ThinkPad, Legion.
        #   https://www.lenovo.com/ar/es/laptops/
        # Dict de salida esperado (Notebook):
        #   {
        #       "modelo": "IdeaPad Gaming 3",
        #       "peso_kg": 2.25, "tamanio_pantalla": 15.6,
        #       "tasa_refresco_hz": 120, "capacidad_bateria_wh": 60,
        #       "imagen_url": "...",
        #       "id_marca": self._id_marca,
        #       "id_categoria": self._id_categoria,
        #   }

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados


class AsusScraper(ScraperEspecificaciones):
    """Specs de notebooks Asus (asus.com)."""

    def __init__(self, id_marca: int, id_categoria: int):
        super().__init__(
            nombre="Asus",
            url_base="https://www.asus.com",
            id_marca=id_marca,
            id_categoria=id_categoria,
        )

    def extraer(self) -> list[dict]:
        self._log_info("Iniciando scraping de Asus...")
        resultados: list[dict] = []

        # TODO: líneas a cubrir -> ROG, TUF, VivoBook, ZenBook.
        #   https://www.asus.com/ar/laptops/

        self._log_info(f"Finalizado: {len(resultados)} productos extraídos.")
        return resultados
