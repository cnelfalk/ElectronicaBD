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
    # Test categories from 1 to 60 (or we can select specific ones)
    # We already know:
    # 58: Laptops
    # 27: AMD CPU
    # 48: Intel CPU
    # 6: GPU (verified)
    # 15: RAM (verified)
    # 14: network adapters
    # Let's test: 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60
    
    cates_to_test = [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 31, 34, 37, 50]
    
    for cate in cates_to_test:
        url = f"https://www.compragamer.com/productos?cate={cate}"
        print(f"\nTesting Category {cate} -> {url}")
        driver.get(url)
        time.sleep(3.5) # wait for angular to load
        
        sopa = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract first 3 product titles
        title_tags = sopa.find_all(class_=lambda c: c and ('title' in c.lower() or 'name' in c.lower())) or sopa.find_all('h3') or sopa.find_all('h2')
        product_names = []
        for tag in title_tags:
            txt = tag.get_text(strip=True)
            if txt and len(txt) > 5 and txt not in product_names:
                product_names.append(txt)
                if len(product_names) >= 3:
                    break
        
        if product_names:
            print(f"  Products in Category {cate}:")
            for name in product_names:
                print(f"    - {name}")
        else:
            print(f"  No products found for Category {cate}")
            
finally:
    driver.quit()
