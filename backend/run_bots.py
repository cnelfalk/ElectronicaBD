"""
Orquestador del motor de scraping de TechMatch.
Ejecutar con: python run_bots.py

ORDEN DE EJECUCION (IMPORTANTE):
1. Fabricantes de laptops (ASUS, Lenovo) → Crean productos con specs tecnicas REALES
2. Fabricantes de componentes (AMD, Intel) → Crean CPUs con specs tecnicas REALES
3. Retailers (MercadoLibre, CompraGamer) → Agregan precios, links e imagenes a productos existentes

Los retailers se ejecutan AL FINAL porque solo guardan precio/link/imagen,
NO crean especificaciones tecnicas. Si se ejecutaran primero, crearian
productos sin specs y luego los fabricantes no podrian actualizarlos correctamente.
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.scrapers_especificaciones import MercadoLibreScraper, CompraGamerScraper
from scrapers.scrapers_fabricantes import AsusScraperLaptops, LenovoScraperLaptops
from scrapers.scrapers_componentes import AMDScraperCPU, IntelScraperCPU
from scrapers.scraper_imagenes import ScraperImagenes


def ejecutarBot(nombre, bot):
    print(f"\n{'='*55}")
    print(f"  INICIANDO: {nombre}")
    print(f"{'='*55}")
    try:
        bot.ejecutarScraping()
        print(f"  [OK] {nombre} finalizado.")
    except Exception as e:
        print(f"  [ERROR] {nombre} fallo: {e}")
        print("  El resto de los bots continuara igual.")
    
    # Pausa de cortesia para evitar bloqueos por rate-limiting
    print("  [INFO] Esperando un momento antes del siguiente bot...")
    time.sleep(6)


if __name__ == "__main__":
    print("\n" + "="*55)
    print("   MOTOR DE SCRAPING TECHMATCH")
    print("="*55)

    # ── PASO 1: Fabricantes de laptops (specs tecnicas reales) ──
    print("\n  >>> FASE 1: Extrayendo specs de fabricantes...")
    ejecutarBot("ASUS Oficial — Laptops",   AsusScraperLaptops())
    ejecutarBot("LENOVO Oficial — Laptops", LenovoScraperLaptops())

    # ── PASO 2: Fabricantes de componentes (specs CPUs) ─────────
    print("\n  >>> FASE 2: Extrayendo specs de componentes...")
    ejecutarBot("AMD — Procesadores",   AMDScraperCPU())
    ejecutarBot("Intel — Procesadores", IntelScraperCPU())

    # ── PASO 3: Retailers (precios + links + imagenes) ──────────
    print("\n  >>> FASE 3: Extrayendo precios de retailers...")

    # --- Laptops ---
    ejecutarBot("MercadoLibre — ASUS",          MercadoLibreScraper("Asus"))
    ejecutarBot("MercadoLibre — LENOVO",         MercadoLibreScraper("Lenovo"))
    ejecutarBot("Compra Gamer — ASUS Laptops",   CompraGamerScraper("Asus",   "Laptop"))
    ejecutarBot("Compra Gamer — LENOVO Laptops", CompraGamerScraper("Lenovo", "Laptop"))

    # --- CPUs ---
    ejecutarBot("Compra Gamer — AMD CPUs",       CompraGamerScraper("AMD",    "CPU"))
    ejecutarBot("Compra Gamer — Intel CPUs",     CompraGamerScraper("Intel",  "CPU"))

    # --- GPUs ---
    ejecutarBot("Compra Gamer — NVIDIA GPUs",    CompraGamerScraper("NVIDIA", "GPU"))
    ejecutarBot("Compra Gamer — AMD GPUs",       CompraGamerScraper("AMD",    "GPU"))

    # --- RAM ---
    ejecutarBot("Compra Gamer — RAM",            CompraGamerScraper("Kingston", "RAM"))

    # --- Almacenamiento ---
    ejecutarBot("Compra Gamer — Almacenamiento", CompraGamerScraper("Kingston", "Almacenamiento"))

    # ── PASO 4: Buscar imágenes faltantes (se ejecuta al final) ─
    print("\n  >>> FASE 4: Buscando imágenes faltantes en MercadoLibre...")
    ejecutarBot("Scraper de Imágenes — MercadoLibre", ScraperImagenes())

    print("\n" + "="*55)
    print("   SCRAPING COMPLETO")
    print("="*55 + "\n")
