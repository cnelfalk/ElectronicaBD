import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scrapers_especificaciones import CompraGamerScraper

print("--- Running CompraGamer GPU bot for NVIDIA ---")
bot_gpu = CompraGamerScraper("NVIDIA", "GPU")
bot_gpu.ejecutarScraping()

print("\n--- Running CompraGamer RAM bot for Kingston ---")
bot_ram = CompraGamerScraper("Kingston", "RAM")
bot_ram.ejecutarScraping()

print("\n--- Running CompraGamer Almacenamiento bot for Kingston ---")
bot_alm = CompraGamerScraper("Kingston", "Almacenamiento")
bot_alm.ejecutarScraping()
