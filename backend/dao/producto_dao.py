from database.conexion import ConexionDB

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
            FROM Productos p
            JOIN Categorias c ON p.id_categoria = c.id_categoria
            JOIN Marcas m ON p.id_marca = m.id_marca
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
                    FROM Productos_Perfiles pp 
                    JOIN Perfiles_Uso pu ON pp.id_perfil = pu.id_perfil 
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
            FROM Productos p
            JOIN Laptops l ON p.id_producto = l.id_producto
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

    # upsertLaptop - Inserta una laptop nueva en el supertipo, su especializacion y su tabla de precios.
    def upsertLaptop(self, modelo, imgUrl, nombreMarca, pesoKg, tamanioPantalla, tasaRefrescoHz, 
                     capacidadBateriaWh, cpuModelo, gpuModelo, ramGb, almacenamientoGb, 
                     precio, urlProducto, nombreTienda):
        
        cursor = self.conexion.cursor(dictionary=True)
        try:
            # 1. Busqueda de Claves Foraneas (Catálogos)
            cursor.execute("SELECT id_marca FROM Marcas WHERE nombre_marca = %s", (nombreMarca,))
            idMarca = cursor.fetchone()['id_marca']
            
            cursor.execute("SELECT id_categoria FROM Categorias WHERE nombre_categoria = 'Laptop'")
            idCategoria = cursor.fetchone()['id_categoria']

            # 2. Insercion en Supertipo (Productos)
            queryProd = "INSERT INTO Productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)"
            cursor.execute(queryProd, (modelo, imgUrl, idMarca, idCategoria))
            idProductoGenerado = cursor.lastrowid 

            # 3. Insercion en Especializacion (Laptops) - Incluye los nuevos campos de rendimiento
            queryLaptop = """
                INSERT INTO Laptops (peso_kg, tamanio_pantalla, tasa_refresco_hz, capacidad_bateria_wh, 
                                     cpu_modelo, gpu_modelo, ram_gb, almacenamiento_gb, id_producto) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(queryLaptop, (pesoKg, tamanioPantalla, tasaRefrescoHz, capacidadBateriaWh, 
                                         cpuModelo, gpuModelo, ramGb, almacenamientoGb, idProductoGenerado))

            # 4. Insercion de la relacion de venta (N:M)
            cursor.execute("SELECT id_tienda FROM Tiendas WHERE nombre_tienda = %s", (nombreTienda,))
            idTienda = cursor.fetchone()['id_tienda']
            
            queryPrecio = "INSERT INTO Se_Vende_En (id_producto, id_tienda, precio, url_producto, fec_actualizacion) VALUES (%s, %s, %s, %s, NOW())"
            cursor.execute(queryPrecio, (idProductoGenerado, idTienda, precio, urlProducto))

            self.conexion.commit() # Si todo sale bien, guardamos los cambios
        except Exception as e:
            self.conexion.rollback() # Si falla cualquier INSERT, revertimos TODO para evitar datos corruptos
            print(f"// errorUpsertLaptop: {e}")
        finally:
            cursor.close()