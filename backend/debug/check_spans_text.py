import os
import sys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_base import ScraperBase

class DummyScraper(ScraperBase):
    def ejecutarScraping(self):
        pass

bot = DummyScraper("test")
driver = bot._crearDriver()
try:
    print("Navigating to products page...")
    driver.get("https://www.compragamer.com/productos")
    time.sleep(12)
    
    print("Listing all spans on page:")
    spans = driver.find_elements(By.TAG_NAME, "span")
    for idx, span in enumerate(spans):
        try:
            txt = span.get_attribute("textContent").strip()
            if txt and len(txt) < 100:
                print(f"Span {idx}: '{txt}'")
        except Exception:
            pass
            
finally:
    driver.quit()
