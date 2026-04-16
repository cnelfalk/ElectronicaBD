"""
scraper_base.py
---------------
Jerarquía base de scrapers para TechMatch.

Diseño OOP:
    ScraperBase (abstracta)
        ├── ScraperPrecios (abstracta)         -> tiendas (Compra Gamer, Mercado Libre)
        └── ScraperEspecificaciones (abstracta)-> fabricantes (AMD, Intel, Lenovo, Asus)

Cada scraper concreto hereda de la abstracta correspondiente e implementa
`extraer()`. La lógica común (HTTP, parseo, logging, manejo de errores)
vive en la clase base para evitar duplicación.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import requests
from bs4 import BeautifulSoup


class ScraperBase(ABC):
    """Clase abstracta raíz. Define el contrato y utilidades HTTP comunes."""

    # Headers para minimizar bloqueos básicos. No es antibot-proof.
    _HEADERS_DEFAULT = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "es-AR,es;q=0.9",
    }

    def __init__(self, nombre: str, url_base: str, timeout: int = 15):
        self._nombre = nombre
        self._url_base = url_base
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(self._HEADERS_DEFAULT)

    # ---- properties (encapsulamiento) -------------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def url_base(self) -> str:
        return self._url_base

    # ---- utilidades compartidas -------------------------------------
    def _obtener_html(self, url: str) -> str:
        """Descarga el HTML de una URL. Retorna string vacío si falla."""
        try:
            resp = self._session.get(url, timeout=self._timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            self._log_error(f"Error al descargar {url}: {e}")
            return ""

    def _parsear(self, html: str) -> BeautifulSoup:
        """Crea un BeautifulSoup con parser lxml (fallback a html.parser)."""
        try:
            return BeautifulSoup(html, "lxml")
        except Exception:
            return BeautifulSoup(html, "html.parser")

    def _log_info(self, msg: str) -> None:
        print(f"[{datetime.now():%H:%M:%S}] [{self._nombre}] {msg}")

    def _log_error(self, msg: str) -> None:
        print(f"[{datetime.now():%H:%M:%S}] [{self._nombre}] ERROR: {msg}")

    # ---- contrato (template method pattern) -------------------------
    @abstractmethod
    def extraer(self) -> list[dict]:
        """
        Ejecuta el scraping y devuelve una lista de dicts con el formato
        propio de cada subtipo (precios vs specs).
        Cada scraper concreto debe implementarlo.
        """
        ...


class ScraperPrecios(ScraperBase):
    """
    Clase abstracta para bots que extraen PRECIOS desde tiendas.
    Formato de salida esperado por cada dict:
        {
            "modelo":       str,
            "precio":       Decimal|float,
            "url_producto": str,
            "id_tienda":    int
        }
    """

    def __init__(self, nombre: str, url_base: str, id_tienda: int):
        super().__init__(nombre, url_base)
        self._id_tienda = id_tienda

    @property
    def id_tienda(self) -> int:
        return self._id_tienda

    @abstractmethod
    def extraer(self) -> list[dict]:
        ...


class ScraperEspecificaciones(ScraperBase):
    """
    Clase abstracta para bots que extraen ESPECIFICACIONES TÉCNICAS
    desde las páginas oficiales de fabricantes.

    Formato de salida esperado por cada dict (según categoría):
        Notebook -> {'modelo','peso_kg','tamanio_pantalla','tasa_refresco_hz','capacidad_bateria_wh','imagen_url'}
        CPU      -> {'modelo','nucleos','hilos','frecuencia_base','frecuencia_turbo','tdp','socket','imagen_url'}
        GPU      -> {'modelo','vram_gb','tipo_memoria','consumo_w','imagen_url'}
    Todos incluyen 'id_marca' y 'id_categoria'.
    """

    def __init__(self, nombre: str, url_base: str, id_marca: int, id_categoria: int):
        super().__init__(nombre, url_base)
        self._id_marca = id_marca
        self._id_categoria = id_categoria

    @property
    def id_marca(self) -> int:
        return self._id_marca

    @property
    def id_categoria(self) -> int:
        return self._id_categoria

    @abstractmethod
    def extraer(self) -> list[dict]:
        ...
