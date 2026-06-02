import os
import sys
import time
import re
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_base import ScraperBase

class DummyScraper(ScraperBase):
    def ejecutarScraping(self):
        pass

bot = DummyScraper("test")
driver = bot._crearDriver()
try:
    print("Navigating to CompraGamer products page...")
    driver.get("https://www.compragamer.com/productos")
    time.sleep(10)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Dump everything related to categories or sidebar
    print("Searching for elements with category information...")
    
    # 1. Print all links that contain 'cate'
    all_links = sopa.find_all('a', href=True)
    print(f"Total links on page: {len(all_links)}")
    for link in all_links:
        href = link['href']
        text = link.get_text(strip=True)
        if 'cate=' in href:
            print(f"LINK: text='{text}' | href='{href}'")
            
    # 2. Print elements that look like filters or categories
    # The sidebar might be inside a custom angular component like <cgw-productos-filtros> or similar
    # Let's search for tags containing "filtro" or "category"
    for tag in sopa.find_all(lambda t: t.name and ('filtro' in t.name or 'category' in t.name or any(c and ('filtro' in c or 'category' in c) for c in t.get('class', [])))):
        print(f"FILTER TAG: name='{tag.name}' | class={tag.get('class')}")
        # print first 200 chars of text
        print(f"   text: {tag.get_text(strip=True)[:200]}")
        
    # 3. Print links that go to /productos
    for link in all_links:
        href = link['href']
        if '/productos' in href and 'cate=' not in href:
            # check if there's any text
            text = link.get_text(strip=True)
            if text:
                print(f"PRODUCTOS LINK: text='{text}' | href='{href}'")

finally:
    driver.quit()
