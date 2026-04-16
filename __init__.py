"""
Paquete `scrapers` — contiene la jerarquía OOP de scrapers de TechMatch.

Exporta las clases concretas para que el orquestador (o un script de
ejecución tipo run_bots.py) las pueda importar directo.
"""

from .scraper_base import (
    ScraperBase,
    ScraperPrecios,
    ScraperEspecificaciones,
)
from .scrapers_precios import CompraGamerScraper, MercadoLibreScraper
from .scrapers_especificaciones import (
    AMDScraper,
    IntelScraper,
    LenovoScraper,
    AsusScraper,
)

__all__ = [
    "ScraperBase",
    "ScraperPrecios",
    "ScraperEspecificaciones",
    "CompraGamerScraper",
    "MercadoLibreScraper",
    "AMDScraper",
    "IntelScraper",
    "LenovoScraper",
    "AsusScraper",
]
