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
    print("Searching for SSD on CompraGamer...")
    driver.get("https://www.compragamer.com/productos?criterio=ssd")
    time.sleep(10)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Dump links containing 'cate' or inspect the products
    links = sopa.find_all('a', href=True)
    print(f"Found {len(links)} links on the search results page.")
    for link in links:
        href = link['href']
        if 'cate=' in href:
            print(f"LINK: text='{link.text.strip()}' | href='{href}'")
            
    # Print first 5 products found
    cards = sopa.find_all('cgw-product-card') or sopa.find_all(class_='product-card')
    print(f"\nFound {len(cards)} products for SSD search:")
    for card in cards[:5]:
        title_tag = card.find(class_='product-card__title') or card.find(class_='product-card__name') or card.find('h3') or card.find('h2') or card.find('p', class_='nombre')
        if title_tag:
            print(f"  - {title_tag.get_text(strip=True)}")
            
finally:
    driver.quit()
