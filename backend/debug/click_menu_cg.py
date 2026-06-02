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
    print("Navigating to CompraGamer products page...")
    driver.get("https://www.compragamer.com/productos")
    time.sleep(8)
    
    # Let's find spans that have category text, and print their attributes
    spans = driver.find_elements(By.TAG_NAME, "span")
    print(f"Found {len(spans)} spans.")
    
    target_texts = ['Discos Sólidos SSD', 'Memorias RAM', 'Placas de Video', 'Procesadores']
    
    # Try to find all links in the page by looking for anything with 'cate='
    # Let's also look for clicks.
    for text in target_texts:
        try:
            print(f"Searching for span with text '{text}'...")
            elements = driver.find_elements(By.XPATH, f"//span[contains(text(), '{text}')]")
            for el in elements:
                try:
                    # Let's print the parent link if any
                    parent = el.find_element(By.XPATH, "..")
                    if parent.tag_name == 'a':
                        print(f"Found direct link parent for '{text}': {parent.get_attribute('href')}")
                    else:
                        print(f"Parent of '{text}' is a '{parent.tag_name}'. Trying to click it...")
                        # Let's click the element or its parent
                        driver.execute_script("arguments[0].click();", el)
                        time.sleep(3)
                        print(f"URL after clicking '{text}': {driver.current_url}")
                except Exception as e:
                    print(f"Error on element for '{text}': {e}")
        except Exception as e:
            print(f"Error searching for '{text}': {e}")
            
finally:
    driver.quit()
