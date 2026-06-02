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
    url = "https://www.compragamer.com/productos?cate=81"
    print(f"Visiting: {url}")
    driver.get(url)
    time.sleep(12)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract product titles
    cards = sopa.find_all('cgw-product-card') or sopa.find_all(class_='product-card')
    print(f"Found {len(cards)} product cards.")
    for idx, card in enumerate(cards):
        title_tag = card.find(class_='product-card__title') or card.find(class_='product-card__name') or card.find('h3') or card.find('h2') or card.find('p', class_='nombre')
        name = title_tag.get_text(strip=True) if title_tag else card.get_text(strip=True)[:100]
        print(f"  {idx+1}: {name}")
        
finally:
    driver.quit()
