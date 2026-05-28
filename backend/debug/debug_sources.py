import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_base import ScraperBase
from bs4 import BeautifulSoup

class DebugScraper(ScraperBase):
    def ejecutarScraping(self):
        pass

    def debug_url(self, name, url):
        print(f"\n=======================================================")
        print(f" DEBUGGING: {name} ({url})")
        print(f"=======================================================")
        driver = self._crearDriver()
        try:
            driver.get(url)
            self._esperar(5, 7)
            html = driver.page_source
            sopa = BeautifulSoup(html, 'html.parser')
            title = sopa.find('title')
            title_text = title.text.strip() if title else 'No Title'
            print(f"  Title: {title_text}")
            
            # Save HTML snapshot for inspection
            filename = f"debug_{name.lower().replace(' ', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  Saved page source to {filename} (length: {len(html)} characters)")
            
            # Try basic element check
            if "compragamer" in url:
                # check CG items
                items = sopa.find_all('div', class_='contenedorPublicacion')
                print(f"  CG: Found {len(items)} with class 'contenedorPublicacion'")
                items_p = sopa.find_all('div', class_=lambda c: c and 'producto' in c.lower())
                print(f"  CG: Found {len(items_p)} with lambda 'producto'")
            elif "amd.com" in url:
                # check AMD items
                items = sopa.find_all('tr', class_=lambda c: c and 'product' in c.lower())
                print(f"  AMD: Found {len(items)} with lambda 'product' in tr")
                items_div = sopa.find_all('div', class_=lambda c: c and 'product' in c.lower())
                print(f"  AMD: Found {len(items_div)} with lambda 'product' in div")
            elif "intel.com" in url:
                # check Intel items
                items = sopa.find_all('div', class_='result-list-item')
                print(f"  Intel: Found {len(items)} with class 'result-list-item'")
                items_tr = sopa.find_all('tr', class_=lambda c: c and 'result' in c.lower())
                print(f"  Intel: Found {len(items_tr)} with lambda 'result' in tr")
            elif "psref.lenovo" in url:
                # check PSREF
                enlaces = sopa.find_all('a', href=True)
                print(f"  PSREF: Found {len(enlaces)} total links.")
                filtered = [a for a in enlaces if '/Product/Lenovo/' in a.get('href', '')]
                print(f"  PSREF: Found {len(filtered)} links matching /Product/Lenovo/")
            elif "lenovo.com/ar" in url:
                # check Lenovo Consumer
                print(f"  Lenovo Consumer: Checking total page length: {len(html)}")

        except Exception as e:
            print(f"  Error debugging {name}: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    d = DebugScraper("Debug")
    d.debug_url("Compra Gamer", "https://www.compragamer.com/?categoria=5")
    d.debug_url("AMD", "https://www.amd.com/es/products/processors/laptop")
    d.debug_url("Intel", "https://ark.intel.com/content/www/us/en/ark/search.html?q=core+i&s=t&OrderBy=Featured")
    d.debug_url("Lenovo PSREF", "https://psref.lenovo.com/Product/Lenovo")
    d.debug_url("Lenovo Consumer", "https://www.lenovo.com/ar/es/laptops/")
