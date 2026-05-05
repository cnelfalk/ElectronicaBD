import sys
import os
directorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(directorio_raiz)

import requests
import re
import time
from bs4 import BeautifulSoup
from dao.producto_dao import ProductoDAO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ScraperLaptopBase - clase padre que define la logica comun de extraccion para laptops
class ScraperLaptopBase:
    # __init__ - inicializa variables de entorno y el DAO
    def __init__(self, marcaDeseada):
        # Atributo marcaDeseada: define si el bot buscara 'Asus' o 'Lenovo'
        self.marcaDeseada = marcaDeseada 
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.dao = ProductoDAO()

    # extraerSpecsDeTexto - analiza un string para deducir RAM, CPU y Almacenamiento
    def extraerSpecsDeTexto(self, tituloProducto):
        specs = {
            "ramGb": 8, # valor por defecto
            "almacenamientoGb": 256, # valor por defecto
            "cpuModelo": "Desconocido",
            "gpuModelo": "Integrada"
        }
        
        tituloLower = tituloProducto.lower()
        
        # extraemos la RAM buscando el patron "16gb" o "16 gb"
        matchRam = re.search(r'(\d+)\s*gb\s*ram?', tituloLower)
        if matchRam:
            specs["ramGb"] = int(matchRam.group(1))

        # extraemos el CPU buscando palabras clave
        if "ryzen 5" in tituloLower: specs["cpuModelo"] = "AMD Ryzen 5"
        elif "ryzen 7" in tituloLower: specs["cpuModelo"] = "AMD Ryzen 7"
        elif "core i5" in tituloLower: specs["cpuModelo"] = "Intel Core i5"
        elif "core i7" in tituloLower: specs["cpuModelo"] = "Intel Core i7"

        return specs

# MercadoLibreScraper - Actualizado con Selenium para evadir bloqueos JS
class MercadoLibreScraper(ScraperLaptopBase):
    def ejecutarScraping(self):
        url = f"https://listado.mercadolibre.com.ar/computacion/laptops-accesorios/notebooks/{self.marcaDeseada.lower()}"
        
        print(f"   [Sistema] Abriendo navegador fantasma para buscar {self.marcaDeseada}...")
        
        # 1. Configurar el navegador Chrome en modo "Incógnito/Fantasma"
        opciones = Options()
        opciones.add_argument('--headless') # Ejecuta Chrome sin abrir la ventana visible
        opciones.add_argument('--disable-gpu')
        opciones.add_argument('--no-sandbox')
        opciones.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 2. Inicializar el driver
        servicio = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=servicio, options=opciones)
        
        try:
            # 3. Entrar a la página
            driver.get(url)
            
            # 4. LA MAGIA: Esperamos 5 segundos a que Mercado Libre ejecute su validación JS
            print("   [Sistema] Esperando a que se resuelva el desafío de seguridad de ML...")
            time.sleep(5) 
            
            # 5. Ahora sí, le pasamos el HTML ya renderizado a BeautifulSoup
            sopa = BeautifulSoup(driver.page_source, 'lxml')
            productosHtml = sopa.find_all('li', class_='ui-search-layout__item')
            
            print(f"   [Debug] Cantidad de productos encontrados reales: {len(productosHtml)}")
            
            if not productosHtml:
                print("   [Error] No se encontraron productos. ML podría haber cambiado la estructura o el bloqueo es más fuerte.")
                return

            for item in productosHtml[:5]:
                try:
                    # FIX 1: Búsqueda del título más agresiva. Buscamos cualquier h2 o h3 dentro de la caja.
                    titulo_tag = item.find('h2') or item.find('h3')
                    if not titulo_tag: 
                        print("   [Debug] Tarjeta ignorada: No se detectó un título válido.")
                        continue
                    modelo = titulo_tag.text.strip()
                    
                    # FIX 2: Búsqueda del precio (ML usa 'andes-money-amount__fraction' casi siempre, pero por las dudas verificamos)
                    precio_tag = item.find('span', class_='andes-money-amount__fraction')
                    if not precio_tag:
                        print(f"   [Debug] Tarjeta ignorada: No se detectó el precio para {modelo}.")
                        continue
                    precioTexto = precio_tag.text.replace('.', '')
                    precioActual = float(precioTexto)
                    
                    # FIX 3: Buscamos el primer enlace de la tarjeta directamente por su etiqueta 'a'
                    enlace_tag = item.find('a')
                    urlVenta = enlace_tag['href'] if enlace_tag and 'href' in enlace_tag.attrs else ""
                    
                    print(f"   [Debug] ¡Encontrado! Guardando en BD: {modelo} - ${precioActual}")
                    
                    # Extracción de specs y guardado
                    specs = self.extraerSpecsDeTexto(modelo)
                    
                    self.dao.upsertLaptop(
                        modelo, "", self.marcaDeseada, 1.8, 15.6, 
                        144 if "gamer" in modelo.lower() else 60, 50, 
                        specs["cpuModelo"], specs["gpuModelo"], specs["ramGb"], specs["almacenamientoGb"],
                        precioActual, urlVenta, "Mercado Libre"
                    )
                except Exception as e:
                    print(f"   [Debug] Error extrayendo el producto: {e}")
                    
        finally:
            # 6. Siempre, SIEMPRE cerrar el navegador al terminar para no consumir toda tu RAM
            driver.quit()

if __name__ == "__main__":
    print("/// Iniciando Motor de Scraping TechMatch ///")
    
    # 1. Instanciamos y ejecutamos el bot para ASUS
    print("-> Buscando laptops ASUS en Mercado Libre...")
    botAsus = MercadoLibreScraper("Asus")
    botAsus.ejecutarScraping()
    
    # 2. Instanciamos y ejecutamos el bot para LENOVO
    print("-> Buscando laptops LENOVO en Mercado Libre...")
    botLenovo = MercadoLibreScraper("Lenovo")
    botLenovo.ejecutarScraping()
    
    print("/// Extracción y Guardado Finalizado Exitosamente ///")