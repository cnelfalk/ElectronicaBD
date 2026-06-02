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
    
    print("Expanding all expansion panels...")
    headers = driver.find_elements(By.TAG_NAME, "mat-expansion-panel-header")
    for h in headers:
        try:
            driver.execute_script("arguments[0].click();", h)
        except Exception as e:
            print(f"Error expanding header: {e}")
    time.sleep(3)
    
    print("Searching spans...")
    spans = driver.find_elements(By.TAG_NAME, "span")
    clicked = False
    for span in spans:
        try:
            txt = span.get_attribute("textContent").strip().lower()
            if "discos" in txt and "ssd" in txt:
                print(f"Found matching span: '{txt}'. Trying to click it...")
                try:
                    driver.execute_script("arguments[0].click();", span)
                    clicked = True
                    print("Click executed. Waiting 5s...")
                    time.sleep(5)
                    print(f"Current URL after clicking: {driver.current_url}")
                    break
                except Exception as click_err:
                    print(f"Error clicking element: {click_err}")
        except Exception as outer_err:
            print(f"Outer error: {outer_err}")
            
    if not clicked:
        print("Could not find or click the span!")
        
finally:
    driver.quit()
