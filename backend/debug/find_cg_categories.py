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
    driver.get("https://www.compragamer.com")
    time.sleep(10) # wait for page to render fully
    
    # Try to find all links with 'cate='
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    links = sopa.find_all('a', href=True)
    
    cate_links = []
    for a in links:
        href = a['href']
        if 'cate=' in href:
            text = a.text.strip().replace('\n', ' ')
            cate_links.append((text, href))
            
    print(f"\nFound {len(cate_links)} links with 'cate=':")
    for text, href in sorted(list(set(cate_links)), key=lambda x: x[1]):
        print(f"Text: '{text}' | Href: '{href}'")
        
finally:
    driver.quit()
