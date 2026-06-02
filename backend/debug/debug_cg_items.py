import sys
import os
import re
import time
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scrapers_especificaciones import CompraGamerScraper

bot = CompraGamerScraper("Kingston", "Almacenamiento")
driver = bot._crearDriver()
try:
    url = f"{bot.BASE_URL}/productos?cate=14"
    driver.get(url)
    bot._esperarRenderizado(driver)
    bot._scrollParaCargar(driver)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    items = bot._extraerCards(sopa)
    print(f"Found {len(items)} cards.")
    
    for i, item in enumerate(items):
        print(f"\n--- Card {i+1} ---")
        # Name
        nombre_tag = (
            item.find(class_='product-card__title') or
            item.find(class_='product-card__name')  or
            item.find('h3') or
            item.find('h2') or
            item.find('p', class_='nombre')
        )
        if not nombre_tag:
            print("No name tag found!")
            continue
        modelo = nombre_tag.get_text(strip=True)
        print(f"Model name: '{modelo}'")
        
        # Check brand terminos
        modelo_lower = modelo.lower()
        aliases = {
            'intel': ['intel', 'core i3', 'core i5', 'core i7', 'core i9', 'core ultra'],
            'nvidia': ['nvidia', 'geforce', 'rtx', 'gtx'],
            'kingston': ['kingston', 'fury', 'hyperx'],
            'amd': ['amd', 'radeon', 'rx '],
        }
        terminos = aliases.get(bot.marca.lower(), [bot.marca.lower()])
        has_brand = any(t in modelo_lower for t in terminos)
        print(f"Has brand '{bot.marca}'? {has_brand}")
        
        # Check exclusions
        has_excl = any(excl in modelo_lower for excl in bot.EXCLUSIONES)
        print(f"Has exclusion? {has_excl}")
        
        # Check category keywords
        has_cat_kw = any(kw in modelo_lower for kw in ['ssd', 'hdd', 'nvme', 'm.2', 'disco'])
        print(f"Has category keywords? {has_cat_kw}")
        
        # Check category exclusions
        has_cat_excl = any(kw in modelo_lower for kw in ['gabinete', 'carcasa', 'carry', 'case', 'adaptador'])
        print(f"Has category exclusions? {has_cat_excl}")
        
        # Price
        precio_tag = (
            item.find(class_='txt_price') or
            item.find(class_=lambda c: c and 'price' in c.lower()
                      and 'old' not in c.lower() and 'before' not in c.lower()) or
            item.find('span', class_='precio')
        )
        if not precio_tag:
            print("No price tag found!")
            continue
        precio_texto = re.sub(r'[^\d,.]', '', precio_tag.get_text(strip=True))
        precio_texto = precio_texto.replace('.', '').replace(',', '.')
        print(f"Price text: '{precio_texto}'")
        
finally:
    driver.quit()
