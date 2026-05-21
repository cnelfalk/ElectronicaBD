import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def test_stealth_ml():
    opciones = Options()
    opciones.add_argument('--headless')
    opciones.add_argument('--disable-gpu')
    opciones.add_argument('--no-sandbox')
    opciones.add_argument('--disable-dev-shm-usage')
    opciones.add_argument('--window-size=1920,1080')
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    opciones.add_argument(f'user-agent={userAgent}')
    
    # Anti-detect options
    opciones.add_argument('--disable-blink-features=AutomationControlled')
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option('useAutomationExtension', False)
    
    try:
        servicio = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=servicio, options=opciones)
    except Exception:
        driver = webdriver.Chrome(options=opciones)
        
    # Execute CDP command to remove webdriver property
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    
    url = "https://listado.mercadolibre.com.ar/computacion/laptops-accesorios/notebooks/asus"
    print(f"Navigating to {url} with stealth settings...")
    try:
        driver.get(url)
        time.sleep(6)
        
        html = driver.page_source
        sopa = BeautifulSoup(html, 'html.parser')
        title = sopa.find('title')
        title_text = title.text.encode('ascii', 'replace').decode('ascii') if title else 'No title'
        print(f"Page Title: {title_text}")
        
        items = sopa.find_all('li', class_='ui-search-layout__item')
        print(f"Items found with 'ui-search-layout__item': {len(items)}")
        
        if len(items) > 0:
            print("SUCCESS: Bypassed safety screen and found products!")
        else:
            print("FAILED: Still blocked or classes changed.")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_stealth_ml()
