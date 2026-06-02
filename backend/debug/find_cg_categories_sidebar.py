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
    time.sleep(10) # wait for page to render fully
    
    # Try to find all links with 'cate=' in the page source
    sopa = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Let's search for elements that look like filters or category selectors
    links = sopa.find_all('a', href=True)
    cate_links = []
    for a in links:
        href = a['href']
        if 'cate=' in href:
            text = a.get_text(strip=True).replace('\n', ' ')
            cate_links.append((text, href))
            
    print(f"\nFound {len(cate_links)} links with 'cate=':")
    for text, href in sorted(list(set(cate_links)), key=lambda x: x[1]):
        print(f"Text: '{text}' | Href: '{href}'")
        
    # Also find buttons or options containing category info
    # e.g., <mat-option>, <mat-select>, check all text with numbers
    print("\nExtracting all text in lists/options that might contain categories:")
    for el in sopa.find_all(['li', 'option', 'span', 'button']):
        txt = el.get_text(strip=True)
        if any(w in txt.lower() for w in ['disco', 'solido', 'ssd', 'memoria', 'ram', 'placa', 'video', 'gpu', 'procesador', 'cpu']):
            if len(txt) < 80:
                print(f"Tag: {el.name} | Text: '{txt}'")
                
finally:
    driver.quit()
