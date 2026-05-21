from database.conexion import ConexionDB
from utils.normalizacion import coincide_modelo, extraer_specs_de_titulo

# ProductoDAO - Capa exclusiva para comunicarse con MySQL. No contiene reglas de negocio.
class ProductoDAO:
    # __init__ - Instancia el Singleton de la base de datos para no saturar conexiones en Laragon.
    def __init__(self):
        self.conexion = ConexionDB.obtenerInstancia()

    # obtenerCatalogoFiltrado - Construye consultas SQL dinamicas para la grilla del frontend.
    # Atributos: categoria (str), perfil (str), busqueda (str)
    def obtenerCatalogoFiltrado(self, categoria=None, perfil=None, busqueda=None):
        query = """
            SELECT 
                p.id_producto, 
                p.modelo_producto as modelo, 
                p.img_url, 
                c.nombre_categoria as categoria, 
                m.nombre_marca as marca
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN marcas m ON p.id_marca = m.id_marca
            WHERE 1=1
        """
        parametrosSql = []

        if categoria:
            query += " AND c.nombre_categoria = %s"
            parametrosSql.append(categoria)

        if busqueda:
            query += " AND p.modelo_producto LIKE %s"
            parametrosSql.append(f"%{busqueda}%")

        if perfil:
            # Subconsulta para evitar duplicados al filtrar relaciones N:M
            query += """
                AND p.id_producto IN (
                    SELECT pp.id_producto 
                    FROM productos_perfiles pp 
                    JOIN perfiles_uso pu ON pp.id_perfil = pu.id_perfil 
                    WHERE pu.nombre_perfil = %s
                )
            """
            parametrosSql.append(perfil)

        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, tuple(parametrosSql))
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Exception as e:
            print(f"// errorObtenerCatalogo: {e}")
            return []

    # obtenerLaptopPorId - Recupera todos los datos fisicos y de rendimiento de una laptop especifica.
    def obtenerLaptopPorId(self, idProducto):
        query = """
            SELECT 
                p.modelo_producto as modelo,
                l.peso_kg, l.tamanio_pantalla, l.tasa_refresco_hz, l.capacidad_bateria_wh,
                l.cpu_modelo, l.gpu_modelo, l.ram_gb, l.almacenamiento_gb
            FROM productos p
            JOIN laptops l ON p.id_producto = l.id_producto
            WHERE p.id_producto = %s
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, (idProducto,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"// errorObtenerLaptop: {e}")
            return None

    # upsertLaptop - Inserta una laptop o actualiza su precio si el modelo ya existe en la BD.
    def upsertLaptop(self, modelo, imgUrl, nombreMarca, pesoKg, tamanioPantalla, tasaRefrescoHz,
                     capacidadBateriaWh, cpuModelo, gpuModelo, ramGb, almacenamientoGb,
                     precio, urlProducto, nombreTienda):

        cursor = self.conexion.cursor(dictionary=True)
        try:
            # Verificar si el modelo ya existe para evitar duplicados
            cursor.execute("SELECT id_producto FROM productos WHERE modelo_producto = %s", (modelo,))
            existente = cursor.fetchone()

            if existente:
                idProducto = existente['id_producto']
                # Actualizar imagen si el producto no tenía una y ahora sí llegó
                if imgUrl:
                    cursor.execute(
                        "UPDATE productos SET img_url = %s WHERE id_producto = %s AND (img_url = '' OR img_url IS NULL)",
                        (imgUrl, idProducto)
                    )
                if precio > 0:
                    cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre_tienda = %s", (nombreTienda,))
                    tiendaRow = cursor.fetchone()
                    if tiendaRow:
                        cursor.execute("""
                            INSERT INTO se_vende_en (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                            VALUES (%s, %s, %s, %s, NOW())
                            ON DUPLICATE KEY UPDATE precio = %s, url_producto = %s, fec_actualizacion = NOW()
                        """, (idProducto, tiendaRow['id_tienda'], precio, urlProducto, precio, urlProducto))
                        self.conexion.commit()
                return

            # Producto nuevo: inserción completa
            cursor.execute("SELECT id_marca FROM marcas WHERE nombre_marca = %s", (nombreMarca,))
            marcaRow = cursor.fetchone()
            if not marcaRow:
                print(f"// upsertLaptop: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaRow['id_marca']

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Laptop'")
            idCategoria = cursor.fetchone()['id_categoria']

            cursor.execute(
                "INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)",
                (modelo, imgUrl, idMarca, idCategoria)
            )
            idProductoGenerado = cursor.lastrowid

            cursor.execute("""
                INSERT INTO laptops (peso_kg, tamanio_pantalla, tasa_refresco_hz, capacidad_bateria_wh,
                                     cpu_modelo, gpu_modelo, ram_gb, almacenamiento_gb, id_producto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (pesoKg, tamanioPantalla, tasaRefrescoHz, capacidadBateriaWh,
                  cpuModelo, gpuModelo, ramGb, almacenamientoGb, idProductoGenerado))

            if precio > 0:
                cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre_tienda = %s", (nombreTienda,))
                tiendaRow = cursor.fetchone()
                if tiendaRow:
                    cursor.execute("""
                        INSERT INTO se_vende_en (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (idProductoGenerado, tiendaRow['id_tienda'], precio, urlProducto))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertLaptop: {e}")
        finally:
            cursor.close()

    # upsertProductoRetail - Inserta o actualiza un producto desde un retailer (ML, CompraGamer).
    # Realiza coincidencia inteligente de modelos para evitar duplicados.
    # Si el producto no coincide con un fabricante oficial, se registra como nuevo.
    # Si es Laptop, autogenera especificaciones técnicas promedio a partir del título.
    def upsertProductoRetail(self, modelo, imgUrl, nombreMarca, nombreCategoria, precio, urlProducto, nombreTienda):
        cursor = self.conexion.cursor(dictionary=True)
        try:
            # Obtener ID de marca y categoría
            cursor.execute("SELECT id_marca FROM marcas WHERE nombre_marca = %s", (nombreMarca,))
            marcaRow = cursor.fetchone()
            if not marcaRow:
                print(f"// upsertProductoRetail: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaRow['id_marca']

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = %s", (nombreCategoria,))
            categoriaRow = cursor.fetchone()
            if not categoriaRow:
                print(f"// upsertProductoRetail: categoría '{nombreCategoria}' no encontrada en BD. Salteando.")
                return
            idCategoria = categoriaRow['id_categoria']

            # Consultar todos los productos cargados en la BD de esa marca y categoría
            cursor.execute(
                "SELECT id_producto, modelo_producto, img_url FROM productos WHERE id_marca = %s AND id_categoria = %s",
                (idMarca, idCategoria)
            )
            productos_existentes = cursor.fetchall()

            idProducto = None
            for prod in productos_existentes:
                if coincide_modelo(modelo, prod['modelo_producto']):
                    idProducto = prod['id_producto']
                    # Actualizar imagen si el producto no tenía una y ahora sí llegó
                    if imgUrl and (not prod['img_url'] or prod['img_url'] == ''):
                        cursor.execute(
                            "UPDATE productos SET img_url = %s WHERE id_producto = %s",
                            (imgUrl, idProducto)
                        )
                    break

            if not idProducto:
                # Producto nuevo: inserción completa
                cursor.execute(
                    "INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)",
                    (modelo, imgUrl, idMarca, idCategoria)
                )
                idProducto = cursor.lastrowid

                # Si es Laptop, insertar en la tabla laptops con especificaciones extraídas y valores por defecto
                if nombreCategoria == 'Laptop':
                    specs = extraer_specs_de_titulo(modelo)
                    cursor.execute("""
                        INSERT INTO laptops (peso_kg, tamanio_pantalla, tasa_refresco_hz, capacidad_bateria_wh,
                                             cpu_modelo, gpu_modelo, ram_gb, almacenamiento_gb, id_producto)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (1.6, 15.6, 60, 45, specs['cpu_modelo'], 'Integrada', specs['ram'], specs['almacenamiento'], idProducto))

            # Insertar o actualizar el precio en la tienda
            if precio > 0:
                cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre_tienda = %s", (nombreTienda,))
                tiendaRow = cursor.fetchone()
                if tiendaRow:
                    cursor.execute("""
                        INSERT INTO se_vende_en (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                        VALUES (%s, %s, %s, %s, NOW())
                        ON DUPLICATE KEY UPDATE precio = %s, url_producto = %s, fec_actualizacion = NOW()
                    """, (idProducto, tiendaRow['id_tienda'], precio, urlProducto, precio, urlProducto))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertProductoRetail: {e}")
        finally:
            cursor.close()

    # upsertCPU - Inserta un procesador o lo saltea si el modelo ya existe.
    def upsertCPU(self, modelo, nucleos, hilos, frecBase, frecTurbo, tdp, urlReferencia):
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_producto FROM productos WHERE modelo_producto = %s", (modelo,))
            if cursor.fetchone():
                return

            nombreMarca = "AMD" if "AMD" in modelo or "Ryzen" in modelo else "Intel"
            cursor.execute("SELECT id_marca FROM marcas WHERE nombre_marca = %s", (nombreMarca,))
            marcaRow = cursor.fetchone()
            if not marcaRow:
                print(f"// upsertCPU: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaRow['id_marca']

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = 'CPU'")
            categoriaRow = cursor.fetchone()
            if not categoriaRow:
                return
            idCategoria = categoriaRow['id_categoria']

            cursor.execute(
                "INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)",
                (modelo, "", idMarca, idCategoria)
            )
            idProducto = cursor.lastrowid

            # Buscar socket por marca: AMD → AM*, Intel → LGA*
            socketKeyword = "AM" if nombreMarca == "AMD" else "LGA"
            cursor.execute("SELECT id_socket FROM socket WHERE nombre_socket LIKE %s LIMIT 1", (f"%{socketKeyword}%",))
            socketRow = cursor.fetchone()
            if not socketRow:
                cursor.execute("SELECT id_socket FROM socket LIMIT 1")
                socketRow = cursor.fetchone()
            if not socketRow:
                print(f"// upsertCPU: no hay sockets en la BD. Salteando {modelo}.")
                self.conexion.rollback()
                return
            idSocket = socketRow['id_socket']

            cursor.execute("""
                INSERT INTO cpu (id_producto, nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp, id_socket)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (idProducto, nucleos, hilos, frecBase, frecTurbo, tdp, idSocket))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertCPU: {e}")
        finally:
            cursor.close()

    # obtenerCPUPorId - Recupera todas las especificaciones de un procesador de la tabla cpu.
    def obtenerCPUPorId(self, idProducto):
        query = """
            SELECT 
                p.modelo_producto as modelo,
                c.nucleos, c.hilos, c.frecuencia_base, c.frecuencia_turbo, c.tdp
            FROM productos p
            JOIN cpu c ON p.id_producto = c.id_producto
            WHERE p.id_producto = %s
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, (idProducto,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"// errorObtenerCPU: {e}")
            return None

    # obtenerCategoriaPorId - Obtiene el nombre de la categoría del producto.
    def obtenerCategoriaPorId(self, idProducto):
        query = """
            SELECT c.nombre_categoria 
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.id_producto = %s
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, (idProducto,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado['nombre_categoria'] if resultado else None
        except Exception as e:
            print(f"// errorObtenerCategoriaPorId: {e}")
            return None

    # obtenerPreciosProducto - Obtiene la lista de precios y enlaces del producto en tiendas.
    def obtenerPreciosProducto(self, idProducto):
        query = """
            SELECT 
                t.nombre_tienda, 
                s.precio, 
                s.url_producto, 
                s.fec_actualizacion
            FROM se_vende_en s
            JOIN tiendas t ON s.id_tienda = t.id_tienda
            WHERE s.id_producto = %s
            ORDER BY s.precio ASC
        """
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(query, (idProducto,))
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print(f"// errorObtenerPreciosProducto: {e}")
            return []