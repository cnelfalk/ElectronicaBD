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
    print("Navigating to CompraGamer products page...")
    driver.get("https://www.compragamer.com/productos")
    time.sleep(12)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    print("\nSearching for span containing 'Sólidos' or 'SSD'...")
    for span in sopa.find_all('span'):
        txt = span.get_text(strip=True)
        if 'sólid' in txt.lower() or 'ssd' in txt.lower() or 'memorias' in txt.lower() or 'procesadores' in txt.lower():
            print(f"\nFound match: '{txt}'")
            print(f"Tag HTML: {span}")
            # Print parents up to 3 levels
            parent = span.parent
            level = 1
            while parent and level <= 3:
                print(f"  Parent L{level}: tag='{parent.name}', class={parent.get('class')}, id={parent.get('id')}, attrs={parent.attrs}")
                parent = parent.parent
                level += 1
                
finally:
    driver.quit()
