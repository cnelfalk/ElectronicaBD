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
    
    # Let's locate the span containing 'Discos Sólidos SSD'
    # Wait, in the output, it was:
    # <span _ngcontent-ng-c1407592627="" class="ng-star-inserted">Discos Sólidos SSD </span>
    # Wait, we might need to expand the parent mat-expansion-panel first if it's hidden!
    # Let's check what mat-expansion-panels exist on the page.
    # In the output of inspect_spans:
    # Found match: 'Discos Sólidos SSD' was inside a mat-expansion-panel-content with role='region' style='height: 0px; visibility: hidden;'
    # That means the expansion panel was CLOSED!
    # We must first click the panel header to expand it!
    # Let's find the header for 'Discos Sólidos SSD''s group. What group is it under?
    # In the output, parent mat-expansion-panel had mat-expansion-panel-header with id 'mat-expansion-panel-header-56'.
    # But id might be dynamic.
    # Let's click the header containing 'Almacenamiento' or something, or let's click the mat-expansion-panel-header that is the parent of the SSD panel.
    # Or even better: we can click all mat-expansion-panel-headers to expand everything, and then click 'Discos Sólidos SSD'!
    
    print("Expanding all expansion panels...")
    headers = driver.find_elements(By.TAG_NAME, "mat-expansion-panel-header")
    print(f"Found {len(headers)} panel headers.")
    for h in headers:
        try:
            driver.execute_script("arguments[0].click();", h)
            time.sleep(0.5)
        except Exception:
            pass
            
    time.sleep(3)
    
    print("Searching for span with text 'Discos Sólidos SSD'...")
    spans = driver.find_elements(By.XPATH, "//span[contains(text(), 'Discos Sólidos') or contains(text(), 'SSD')]")
    print(f"Found {len(spans)} matching spans.")
    
    clicked = False
    for span in spans:
        txt = span.text.strip()
        print(f"Span text: '{txt}'")
        if 'sólidos' in txt.lower() or 'ssd' in txt.lower():
            print(f"Clicking span: '{txt}'")
            try:
                driver.execute_script("arguments[0].click();", span)
                clicked = True
                time.sleep(5)
                print(f"Current URL after clicking: {driver.current_url}")
                break
            except Exception as e:
                print(f"Failed to click: {e}")
                
    if not clicked:
        print("Could not find or click the span!")
        
finally:
    driver.quit()
