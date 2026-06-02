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
    print("Navigating to SSD search...")
    driver.get("https://www.compragamer.com/productos?criterio=ssd")
    time.sleep(10)
    
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the first product link
    cards = sopa.find_all('cgw-product-card') or sopa.find_all(class_='product-card')
    product_url = None
    for card in cards:
        anchor = card if card.name == 'a' else card.find('a', href=True)
        if anchor and anchor.get('href'):
            href = anchor['href']
            product_url = f"https://www.compragamer.com{href}" if href.startswith('/') else href
            break
            
    if not product_url:
        # try simple search for link with /producto/
        for a in sopa.find_all('a', href=True):
            href = a['href']
            if '/producto/' in href:
                product_url = f"https://www.compragamer{href}" if href.startswith('/') else href
                break
                
    if product_url:
        print(f"Visiting product detail: {product_url}")
        driver.get(product_url)
        time.sleep(8)
        
        detail_sopa = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Check all links with 'cate='
        print("\nChecking all links with 'cate=' on detail page:")
        links = detail_sopa.find_all('a', href=True)
        for link in links:
            href = link['href']
            if 'cate=' in href:
                print(f"LINK: text='{link.text.strip()}' | href='{href}'")
    else:
        print("No product URL found!")
        
finally:
    driver.quit()
