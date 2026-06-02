import os
import sys
import time
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_base import ScraperBase

class DummyScraper(ScraperBase):
    def ejecutarScraping(self):
        pass

bot = DummyScraper("test")
driver = bot._crearDriver()
try:
    url = "https://www.compragamer.com/producto/Disco_Solido_SSD_M_2_Sandisk_1TB_Plus_3200MB_s_NVMe_PCI_E_Gen3_x4_18107?criterio=ssd"
    print(f"Visiting product detail: {url}")
    driver.get(url)
    time.sleep(8)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    print("\nAll links on page:")
    links = sopa.find_all('a', href=True)
    print(f"Total links found: {len(links)}")
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        if any(keyword in href for keyword in ['productos', 'cate', 'sec']):
            print(f"LINK: text='{text}' | href='{href}'")
        elif 'discos' in text.lower() or 'ssd' in text.lower() or 'almacen' in text.lower():
            print(f"SSD/ALMACENAMIENTO LINK: text='{text}' | href='{href}'")
            
finally:
    driver.quit()
