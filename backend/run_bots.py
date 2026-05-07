"""
Orquestador del motor de scraping de TechMatch.
Ejecutar con: python run_bots.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.scrapers_especificaciones import MercadoLibreScraper, CompraGamerScraper
from scrapers.scrapers_fabricantes import AsusScraperLaptops, LenovoScraperLaptops
from scrapers.scrapers_componentes import AMDScraperCPU, IntelScraperCPU


def ejecutarBot(nombre, bot):
    print(f"\n{'='*55}")
    print(f"  INICIANDO: {nombre}")
    print(f"{'='*55}")
    try:
        bot.ejecutarScraping()
        print(f"  [OK] {nombre} finalizado.")
    except Exception as e:
        print(f"  [ERROR] {nombre} falló: {e}")
        print("  El resto de los bots continuará igual.")


if __name__ == "__main__":
    print("\n" + "="*55)
    print("   MOTOR DE SCRAPING TECHMATCH")
    print("="*55)

    # ── Retailers (precios) ──────────────────────────────
    ejecutarBot("MercadoLibre — ASUS",   MercadoLibreScraper("Asus"))
    ejecutarBot("MercadoLibre — LENOVO", MercadoLibreScraper("Lenovo"))
    ejecutarBot("Compra Gamer — ASUS",   CompraGamerScraper("Asus"))
    ejecutarBot("Compra Gamer — LENOVO", CompraGamerScraper("Lenovo"))

    # ── Fabricantes de laptops (specs) ───────────────────
    ejecutarBot("ASUS Oficial",   AsusScraperLaptops())
    ejecutarBot("LENOVO Oficial", LenovoScraperLaptops())

    # ── Fabricantes de componentes (specs CPUs) ──────────
    ejecutarBot("AMD — Procesadores",   AMDScraperCPU())
    ejecutarBot("Intel — Procesadores", IntelScraperCPU())

    print("\n" + "="*55)
    print("   SCRAPING COMPLETO")
    print("="*55 + "\n")
