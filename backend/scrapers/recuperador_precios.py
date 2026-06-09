import sys
import os
import time
import urllib.parse
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapers.scraper_base import ScraperBase
from utils.normalizacion import validar_url_retail
from dao.tienda_dao import TiendaDAO

class RecuperadorPrecios(ScraperBase):
    def __init__(self):
        super().__init__("Varios")
        self.TIENDA = "Mercado Libre"

    def ejecutarScraping(self):
        query = """
            SELECT p.id_producto, p.modelo_producto, m.nombre_marca, c.nombre_categoria
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN marcas m ON p.id_marca = m.id_marca
            LEFT JOIN producto_tienda s ON p.id_producto = s.id_producto
            WHERE s.id_producto IS NULL
        """
        # Obtenemos los huerfanos usando el cursor del dao
        cursor = self.dao.conexion.cursor(dictionary=True)
        cursor.execute(query)
        huerfanos = cursor.fetchall()
        cursor.close()
        
        huerfanos_a_procesar = huerfanos
        print(f"Productos sin precio encontrados: {len(huerfanos_a_procesar)}")
        
        driver = self._crearDriver()
        try:
            for idx, item in enumerate(huerfanos_a_procesar):
                modelo_db = item['modelo_producto']
                marca = item['nombre_marca']
                categoria = item['nombre_categoria']
                
                # Extraemos solo palabras clave importantes para que la búsqueda sea efectiva
                # Por ejemplo, remover "Notebook", "Laptop", y quedarnos con la linea (Vivobook X1404)
                query_limpia = modelo_db.replace("Notebook", "").replace("Laptop", "").replace("processor", "").replace("Processor", "").strip()
                # Cortar en 6 palabras para no hacer la busqueda tan especifica que ML falle
                palabras = query_limpia.split()[:6]
                query_ml = " ".join(palabras)
                
                busqueda = f"{marca} {query_ml}"
                url = f"https://listado.mercadolibre.com.ar/{urllib.parse.quote(busqueda)}"
                
                print(f"\n[{idx+1}/{len(huerfanos_a_procesar)}] Buscando: {busqueda}")
                
                driver.get(url)
                time.sleep(3) # Esperar a ML
                
                sopa = BeautifulSoup(driver.page_source, 'html.parser')
                resultados = sopa.find_all('li', class_='ui-search-layout__item')
                
                encontrado = False
                for res in resultados[:3]:
                    titulo_tag = res.find('h2') or res.find('h3')
                    if not titulo_tag: continue
                    titulo_ml = titulo_tag.text.strip()
                    
                    if "usado" in res.text.lower(): continue
                    if "funda" in titulo_ml.lower() or "teclado" in titulo_ml.lower() or "cargador" in titulo_ml.lower(): continue
                    
                    precio_tag = res.find('span', class_='andes-money-amount__fraction')
                    if not precio_tag: continue
                    precio = float(precio_tag.text.replace('.', '').replace(',', '.'))
                    
                    enlace_tag = res.find('a')
                    urlVenta = enlace_tag['href'] if enlace_tag else ""
                    if '?' in urlVenta: urlVenta = urlVenta.split('?')[0]
                    if not validar_url_retail(urlVenta, self.TIENDA): continue
                    
                    img_tag = res.find('img', class_='ui-search-result-image__element') or res.find('img')
                    imgUrl = ""
                    if img_tag:
                        imgUrl = img_tag.get('data-src') or img_tag.get('src', '')
                        if not imgUrl.startswith('http'): imgUrl = ""
                    
                    print(f"  -> Match encontrado en ML: {titulo_ml[:60]}... - ${precio}")
                    
                    # Insertamos el precio directamente al ID del producto huerfano
                    id_producto = item['id_producto']
                    cursor = self.dao.conexion.cursor(dictionary=True)
                    try:
                        tiendaObj = TiendaDAO().obtenerTiendaPorNombre(self.TIENDA)
                        if tiendaObj:
                            cursor.execute("""
                                INSERT INTO producto_tienda (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                                VALUES (%s, %s, %s, %s, NOW())
                                ON DUPLICATE KEY UPDATE precio = %s, url_producto = %s, fec_actualizacion = NOW()
                            """, (id_producto, tiendaObj.idTienda, precio, urlVenta, precio, urlVenta))
                            self.dao.conexion.commit()
                            
                            # Actualizar imagen si el producto no tenia
                            cursor.execute(
                                "UPDATE productos SET img_url = %s WHERE id_producto = %s AND (img_url = '' OR img_url IS NULL)",
                                (imgUrl, id_producto)
                            )
                            self.dao.conexion.commit()
                            
                    except Exception as e:
                        print(f"  [Error SQL] {e}")
                    finally:
                        cursor.close()
                    
                    encontrado = True
                    break # Con uno nos alcanza para asignar precio
                
                if not encontrado:
                    print("  -> Sin match valido o sin precios en top 3 de resultados.")
                
                self._esperar(0.5, 1.5)
                
        finally:
            driver.quit()

if __name__ == "__main__":
    bot = RecuperadorPrecios()
    bot.ejecutarScraping()
