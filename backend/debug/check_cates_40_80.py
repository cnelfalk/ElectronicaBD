import os
import sys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_base import ScraperBase

class DummyScraper(ScraperBase):
    def ejecutarScraping(self):
        pass

bot = DummyScraper("test")
driver = bot._crearDriver()
try:
    cates = [c for c in range(40, 81) if c not in [48, 58]]
    
    print("Starting category sweep from 40 to 80...")
    for cate in cates:
        url = f"https://www.compragamer.com/productos?cate={cate}"
        driver.get(url)
        
        has_products = False
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                    "cgw-product-card, app-product-card, a[href*='/producto/']"
                ))
            )
            has_products = True
        except Exception:
            pass
            
        if has_products:
            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            cards = sopa.find_all('cgw-product-card') or sopa.find_all(class_='product-card')
            if not cards:
                cards = sopa.find_all('a', href=lambda h: h and '/producto/' in h)
                
            product_names = []
            for card in cards[:3]:
                title_tag = card.find(class_='product-card__title') or card.find(class_='product-card__name') or card.find('h3') or card.find('h2') or card.find('p', class_='nombre')
                if title_tag:
                    product_names.append(title_tag.get_text(strip=True))
                else:
                    product_names.append(card.get_text(strip=True)[:60])
                    
            print(f"Category {cate} (FOUND products):")
            for name in product_names[:3]:
                print(f"  - {name}")
        else:
            pass
            
finally:
    driver.quit()
