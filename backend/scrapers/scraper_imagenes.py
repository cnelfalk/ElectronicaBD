"""
scraper_imagenes.py — Buscador de imágenes para productos sin foto.

Busca en MercadoLibre Argentina una imagen real para cada producto
que tiene img_url vacío o NULL en la base de datos.

Ejecutar con:
    python scrapers/scraper_imagenes.py

O importar y usar desde run_bots.py:
    from scrapers.scraper_imagenes import ScraperImagenes
    ScraperImagenes().ejecutarScraping()
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import re
from bs4 import BeautifulSoup
from scrapers.scraper_base import ScraperBase


class ScraperImagenes(ScraperBase):
    """
    Scraper especializado en buscar imágenes reales de productos.
    
    Estrategia:
    1. Consultar la BD para obtener todos los productos sin imagen.
    2. Para cada producto, buscar en MercadoLibre usando el modelo como query.
    3. Extraer la imagen del primer resultado relevante.
    4. Actualizar la columna img_url en la tabla productos.
    """

    # Categorías de búsqueda en MercadoLibre por categoría de producto
    RUTAS_ML = {
        'CPU': 'computacion/componentes-pc/procesadores',
        'GPU': 'computacion/componentes-pc/placas-video',
        'RAM': 'computacion/componentes-pc/memorias-ram',
        'Laptop': 'computacion/laptops-accesorios/notebooks',
        'Almacenamiento': 'computacion/componentes-pc/discos-accesorios',
    }

    def __init__(self):
        super().__init__("ImageFinder")

    def ejecutarScraping(self):
        """Busca imágenes para todos los productos sin foto en la BD."""
        print("\n  [IMG] Buscando productos sin imagen en la base de datos...")

        # obtenerProductosSinImagen - consulta la BD por productos con img_url vacío
        productosSinImagen = self._obtenerProductosSinImagen()
        total = len(productosSinImagen)

        if total == 0:
            print("  [IMG] ¡Todos los productos ya tienen imagen! No hay nada que hacer.")
            return

        print(f"  [IMG] {total} productos sin imagen encontrados. Iniciando búsqueda...\n")

        driver = self._crearDriver()
        actualizados = 0
        errores = 0

        try:
            for i, producto in enumerate(productosSinImagen, 1):
                idProducto = producto['id_producto']
                modelo = producto['modelo_producto']
                categoria = producto['nombre_categoria']
                marca = producto['nombre_marca']

                print(f"  [IMG] ({i}/{total}) Buscando imagen para: {modelo[:65]}...")

                try:
                    # Recrear driver periodicamente para evitar problemas de sesion / degradacion de Selenium
                    if i > 1 and i % 25 == 0:
                        print("  [IMG]   Reiniciando WebDriver preventivamente para mantener la estabilidad...")
                        try:
                            driver.quit()
                        except:
                            pass
                        driver = self._crearDriver()

                    imgUrl = self._buscarImagenEnML(driver, modelo, categoria, marca)

                    if imgUrl:
                        exito = self._actualizarImagen(idProducto, imgUrl)
                        if exito:
                            actualizados += 1
                            print(f"  [IMG]   OK: Imagen encontrada y guardada.")
                        else:
                            errores += 1
                            print(f"  [IMG]   WARN: Imagen encontrada pero fallo la actualizacion en BD.")
                    else:
                        print(f"  [IMG]   ERR: No se encontro imagen relevante.")

                    # Pausa entre búsquedas para no sobrecargar ML
                    self._esperar(2, 4)

                except Exception as e:
                    errores += 1
                    print(f"  [IMG]   ERR: Error: {e}")
                    if "session" in str(e).lower() or "driver" in str(e).lower() or "invalid session" in str(e).lower():
                        print("  [IMG]   Recreando WebDriver debido a un error de sesion...")
                        try:
                            driver.quit()
                        except:
                            pass
                        try:
                            driver = self._crearDriver()
                        except Exception as de:
                            print(f"  [IMG]   ERR: No se pudo recrear el driver: {de}")
                    self._esperar(3, 5)

        finally:
            driver.quit()

        print(f"\n  [IMG] ========================================")
        print(f"  [IMG] Resumen: {actualizados} imagenes actualizadas, {errores} errores, {total - actualizados - errores} sin resultado.")
        print(f"  [IMG] ========================================\n")

    def _obtenerProductosSinImagen(self):
        """Consulta la BD por productos con img_url NULL o vacío."""
        query = """
            SELECT 
                p.id_producto,
                p.modelo_producto,
                c.nombre_categoria,
                m.nombre_marca
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.img_url IS NULL OR p.img_url = ''
            ORDER BY c.nombre_categoria, p.modelo_producto
        """
        cursor = self.dao.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"  [IMG] Error consultando BD: {e}")
            return []
        finally:
            cursor.close()

    def _buscarImagenEnML(self, driver, modelo, categoria, marca):
        """
        Busca una imagen del producto en MercadoLibre Argentina.
        
        Estrategia:
        1. Construir URL de búsqueda usando la categoría correcta de ML.
        2. Buscar por modelo completo.
        3. Si no encuentra, simplificar el query (quitar palabras genéricas).
        4. Extraer la imagen del primer resultado.
        """
        # limpiarQueryBusqueda - simplificar el modelo para búsqueda efectiva
        queryBusqueda = self._limpiarQueryBusqueda(modelo, marca)

        # URL original que funcionaba (sin ruta de categoría en el path)
        urlBusqueda = f"https://listado.mercadolibre.com.ar/{queryBusqueda.replace(' ', '-')}_ItemType*id_N_NoIndex_True"

        try:
            driver.get(urlBusqueda)
            time.sleep(4)

            sopa = BeautifulSoup(driver.page_source, 'html.parser')
            items = sopa.find_all('li', class_='ui-search-layout__item')

            if not items:
                # Fallback sin el filtro _ItemType
                urlFallback = f"https://listado.mercadolibre.com.ar/{queryBusqueda.replace(' ', '-')}"
                driver.get(urlFallback)
                time.sleep(4)
                sopa = BeautifulSoup(driver.page_source, 'html.parser')
                items = sopa.find_all('li', class_='ui-search-layout__item')

            if not items:
                return None

            # Validar por título (h2) para evitar fotos de otra categoría
            for item in items[:8]:
                if "usado" in item.text.lower():
                    continue
                tituloTag = item.find('h2') or item.find('a', class_=lambda c: c and 'title' in c)
                tituloTexto = tituloTag.get_text(strip=True) if tituloTag else ''
                # Solo filtramos si obtuvimos un título real; si está vacío, aceptamos
                if tituloTexto and not self._tituloEsCoherente(tituloTexto, categoria):
                    continue
                imgUrl = self._extraerImagenDeItem(item)
                if imgUrl:
                    return imgUrl


            return None

        except Exception as e:
            print(f"  [IMG]   Error en búsqueda ML: {e}")
            return None

    def _tituloEsCoherente(self, textoItem, categoria):
        """
        Verifica que el título de un resultado de ML corresponde a la categoría esperada.
        Evita que una búsqueda de CPU devuelva imágenes de notebooks, etc.
        """
        texto = textoItem.lower()

        # Palabras que NO deben aparecer en el TÍTULO según la categoría
        # (solo frases claras de otra categoría, no términos ambiguos)
        EXCLUSIONES = {
            'CPU':            ['notebook', 'laptop', 'placa de video'],
            'GPU':            ['notebook', 'laptop', 'memoria ram'],
            'RAM':            ['notebook', 'laptop', 'placa de video', 'pendrive'],
            'Almacenamiento': ['notebook', 'laptop', 'memoria ram', 'placa de video', 'pendrive'],
            'Laptop':         ['placa de video geforce', 'placa de video radeon', 'memoria ram ddr'],
        }

        # Al menos una de estas palabras debe aparecer en el título
        REQUERIDAS = {
            'CPU':            ['procesador', 'ryzen', 'core i', 'intel core', 'athlon', 'celeron', 'pentium', 'core ultra', 'amd ryzen'],
            'GPU':            ['placa de video', 'geforce', 'radeon rx', 'rtx', 'gtx'],
            'RAM':            ['memoria ram', 'ddr4', 'ddr5', 'memoria ddr'],
            'Almacenamiento': ['ssd', 'disco solido', 'nvme', 'disco rigido'],
            'Laptop':         ['notebook', 'laptop'],
        }

        exclusiones = EXCLUSIONES.get(categoria, [])
        requeridas  = REQUERIDAS.get(categoria, [])

        # Rechazar si contiene palabras de categoría incorrecta
        if any(ex in texto for ex in exclusiones):
            return False

        # Aceptar solo si contiene al menos una palabra esperada (si hay lista)
        if requeridas and not any(req in texto for req in requeridas):
            return False

        return True

    def _limpiarQueryBusqueda(self, modelo, marca):
        """
        Simplifica el nombre del modelo para obtener mejores resultados de búsqueda.
        Ejemplo: 'ASUS Vivobook 15 OLED X1505VA-MA344W' → 'ASUS Vivobook 15 OLED'
        """
        query = modelo

        # Remover códigos de parte largos (ej: X1505VA-MA344W, 100-100001491BOX)
        query = re.sub(r'\b[A-Z0-9]{4,}-[A-Z0-9]{3,}\b', '', query)
        
        # Remover códigos sueltos alfanuméricos largos que parecen SKUs
        query = re.sub(r'\b[A-Z]{1,3}\d{4,}\w*\b', '', query)

        # Remover paréntesis y su contenido (suelen ser aclaraciones técnicas)
        query = re.sub(r'\([^)]*\)', '', query)

        # Limpiar espacios múltiples
        query = re.sub(r'\s+', ' ', query).strip()

        # Si el query quedó muy corto, usar el modelo original
        if len(query) < 8:
            query = modelo

        return query

    def _extraerImagenDeItem(self, item):
        """Extrae la URL de imagen de un item de resultado de MercadoLibre."""
        # ML usa img con clase ui-search-result-image__element
        img_tag = item.find('img', class_='ui-search-result-image__element')
        if not img_tag:
            img_tag = item.find('img')

        if not img_tag:
            return None

        # ML usa data-src para lazy loading, src como fallback
        imgUrl = img_tag.get('data-src') or img_tag.get('src', '')

        # Validar que sea una URL real de imagen
        if not imgUrl.startswith('http'):
            return None

        # Ignorar placeholders y SVGs
        if 'data:image' in imgUrl or '.svg' in imgUrl:
            return None

        # Mejorar calidad: ML sirve thumbnails por defecto.
        # Reemplazar tamaño pequeño por uno más grande si es posible.
        imgUrl = self._mejorarCalidadImagen(imgUrl)

        return imgUrl

    def _mejorarCalidadImagen(self, imgUrl):
        """
        MercadoLibre sirve imágenes en diferentes tamaños usando sufijos:
        -I.jpg (original), -O.jpg (grande), -D.jpg (mediano), -F.jpg (pequeño)
        Intentamos obtener la versión mediana-grande.
        """
        # Reemplazar sufijos de tamaño por uno más grande
        imgUrl = re.sub(r'-[A-Z]\.jpg$', '-O.jpg', imgUrl)
        imgUrl = re.sub(r'-[A-Z]\.webp$', '-O.webp', imgUrl)
        return imgUrl

    def _actualizarImagen(self, idProducto, imgUrl):
        """Actualiza la columna img_url del producto en la base de datos."""
        cursor = self.dao.conexion.cursor()
        try:
            cursor.execute(
                "UPDATE productos SET img_url = %s WHERE id_producto = %s AND (img_url IS NULL OR img_url = '')",
                (imgUrl, idProducto)
            )
            self.dao.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.dao.conexion.rollback()
            print(f"  [IMG]   Error actualizando BD: {e}")
            return False
        finally:
            cursor.close()


# -- Ejecucion directa ------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("   SCRAPER DE IMAGENES - TECHMATCH")
    print("=" * 55)

    scraper = ScraperImagenes()
    scraper.ejecutarScraping()

    print("=" * 55)
    print("   SCRAPING DE IMAGENES COMPLETO")
    print("=" * 55 + "\n")
