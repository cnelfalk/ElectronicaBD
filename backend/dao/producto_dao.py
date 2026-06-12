from database.conexion import ConexionDB
from utils.normalizacion import coincide_modelo, extraer_specs_de_titulo, extraer_specs_gpu, extraer_specs_ram, extraer_specs_almacenamiento, validar_url_retail
from modelos.producto import Producto
from modelos.laptop import Laptop
from modelos.cpu import CPU
from modelos.gpu import GPU
from modelos.ram import RAM
from modelos.almacenamiento import Almacenamiento
from dao.marca_dao import MarcaDAO
from dao.categoria_dao import CategoriaDAO
from dao.tienda_dao import TiendaDAO

# ProductoDAO - Capa exclusiva para comunicarse con MySQL. No contiene reglas de negocio.
class ProductoDAO:
    @property
    def conexion(self):
        return ConexionDB.obtenerInstancia()

    # obtenerCatalogoFiltrado - Construye consultas SQL dinamicas para la grilla del frontend.
    # Atributos: categoria (str), perfil (str), busqueda (str), marca (str), ordenar (str)
    def obtenerCatalogoFiltrado(self, categoria=None, perfil=None, busqueda=None, marca=None, ordenar=None):
        # esPopulares - determina si el usuario quiere ver los productos más guardados como favorito
        esPopulares = (ordenar == 'populares')

        query = """
            SELECT 
                p.id_producto, 
                p.modelo_producto as modelo, 
                p.img_url, 
                c.nombre_categoria as categoria, 
                m.nombre_marca as marca
        """

        # agregarConteoFavoritos - si se ordena por popularidad, agregamos el conteo
        if esPopulares:
            query += ", COALESCE(fav_count.total, 0) as total_favoritos"

        query += """
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN marcas m ON p.id_marca = m.id_marca
        """

        # joinFavoritos - LEFT JOIN con subconsulta de conteo de favoritos
        if esPopulares:
            query += """
                LEFT JOIN (
                    SELECT id_producto, COUNT(*) as total
                    FROM guarda_favorito
                    GROUP BY id_producto
                ) fav_count ON p.id_producto = fav_count.id_producto
            """

        query += " WHERE 1=1"
        parametrosSql = []

        if categoria:
            query += " AND c.nombre_categoria = %s"
            parametrosSql.append(categoria)

        if busqueda:
            query += " AND p.modelo_producto LIKE %s"
            parametrosSql.append(f"%{busqueda}%")

        if marca:
            query += " AND m.nombre_marca = %s"
            parametrosSql.append(marca)

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

        # ordenarResultados - si es popular, ordena por cantidad de favoritos descendente
        if esPopulares:
            query += " ORDER BY total_favoritos DESC, p.modelo_producto ASC"
        else:
            query += " ORDER BY p.modelo_producto ASC"

        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, tuple(parametrosSql))
            rows = cursor.fetchall()
            productos = []
            for row in rows:
                p = Producto(
                    idProducto=row['id_producto'],
                    modeloProducto=row['modelo'],
                    imgUrl=row['img_url'],
                    urlOficial=None,
                    idCategoria=None,
                    idMarca=None
                )
                p.categoria = row['categoria']
                p.marca = row['marca']
                if 'total_favoritos' in row:
                    p.total_favoritos = row['total_favoritos']
                productos.append(p)
            return productos
        except Exception as e:
            print(f"// errorObtenerCatalogo: {e}")
            return []
        finally:
            cursor.close()

    # obtenerLaptopPorId - Recupera todos los datos fisicos y de rendimiento de una laptop especifica.
    def obtenerLaptopPorId(self, idProducto):
        query = """
            SELECT 
                p.id_producto, p.modelo_producto, p.img_url, p.id_categoria, p.id_marca,
                c.nombre_categoria as categoria, m.nombre_marca as marca,
                l.peso_kg, l.tamanio_pantalla, l.tasa_refresco_hz, l.capacidad_bateria_wh,
                l.cpu_modelo, l.gpu_modelo, l.ram_gb, l.almacenamiento_gb
            FROM productos p
            JOIN laptops l ON p.id_producto = l.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            row = cursor.fetchone()
            if not row:
                return None
            laptop = Laptop(
                idProducto=row['id_producto'],
                modeloProducto=row['modelo_producto'],
                imgUrl=row['img_url'],
                urlOficial=None,
                idCategoria=row['id_categoria'],
                idMarca=row['id_marca'],
                cpuObj=row['cpu_modelo'],
                gpuObj=row['gpu_modelo'],
                ramObj=row['ram_gb'],
                almacenamientoObj=row['almacenamiento_gb'],
                pesoKg=row['peso_kg'],
                tamanioPantalla=row['tamanio_pantalla'],
                tasaRefrescoHz=row['tasa_refresco_hz'],
                capacidadBateriaWh=row['capacidad_bateria_wh']
            )
            laptop.categoria = row['categoria']
            laptop.marca = row['marca']
            return laptop
        except Exception as e:
            print(f"// errorObtenerLaptop: {e}")
            return None
        finally:
            cursor.close()

    # upsertLaptop - Inserta una laptop o actualiza su precio si el modelo ya existe en la BD.
    def upsertLaptop(self, modelo, imgUrl, nombreMarca, pesoKg, tamanioPantalla, tasaRefrescoHz,
                     capacidadBateriaWh, cpuModelo, gpuModelo, ramGb, almacenamientoGb,
                     precio, urlProducto, nombreTienda):

        if not cpuModelo or cpuModelo.strip() == "" or cpuModelo.lower() in ["desconocido", "none", "null"]:
            print(f"// upsertLaptop: Laptop '{modelo}' salteada por no tener un procesador definido.")
            return

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
                    if validar_url_retail(urlProducto, nombreTienda):
                        cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre_tienda = %s", (nombreTienda,))
                        tiendaRow = cursor.fetchone()
                        if tiendaRow:
                            cursor.execute("""
                                INSERT INTO producto_tienda (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                                VALUES (%s, %s, %s, %s, NOW())
                                ON DUPLICATE KEY UPDATE precio = %s, url_producto = %s, fec_actualizacion = NOW()
                            """, (idProducto, tiendaRow['id_tienda'], precio, urlProducto, precio, urlProducto))
                            self.conexion.commit()
                    else:
                        print(f"// upsertLaptop: Enlace invalido para {nombreTienda}: '{urlProducto}'. Salteando guardado de precio.")
                return

            # Producto nuevo: inserción completa
            marcaObj = MarcaDAO().obtenerMarcaPorId_nombre(nombreMarca)
            if not marcaObj:
                print(f"// upsertLaptop: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaObj.idMarca

            categoriaObj = CategoriaDAO().obtenerCategoriaPorNombre('Laptop')
            idCategoria = categoriaObj.idCategoria

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
                if validar_url_retail(urlProducto, nombreTienda):
                    tiendaObj = TiendaDAO().obtenerTiendaPorNombre(nombreTienda)
                    if tiendaObj:
                        cursor.execute("""
                            INSERT INTO producto_tienda (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                            VALUES (%s, %s, %s, %s, NOW())
                        """, (idProductoGenerado, tiendaObj.idTienda, precio, urlProducto))
                else:
                    print(f"// upsertLaptop: Enlace invalido para {nombreTienda}: '{urlProducto}'. Salteando guardado de precio.")

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
            # Obtener ID de marca y categoría usando los DAOs especializados
            marcaObj = MarcaDAO().obtenerMarcaPorId_nombre(nombreMarca)
            if not marcaObj:
                print(f"// upsertProductoRetail: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaObj.idMarca

            categoriaObj = CategoriaDAO().obtenerCategoriaPorNombre(nombreCategoria)
            if not categoriaObj:
                print(f"// upsertProductoRetail: categoría '{nombreCategoria}' no encontrada en BD. Salteando.")
                return
            idCategoria = categoriaObj.idCategoria

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
                    # repararHuerfano - Si el producto existe pero le faltan specs, insertamos valores por defecto
                    self._repararSpecsSiFaltan(cursor, idProducto, nombreCategoria, modelo)
                    break

            if not idProducto:
                # Validar calidad antes de crear un nuevo producto
                if nombreCategoria == 'Laptop':
                    specs = extraer_specs_de_titulo(modelo)
                    cpu = specs.get('cpu_modelo')
                    if not cpu or cpu.strip() == "" or cpu.lower() in ["desconocido", "none", "null"]:
                        print(f"// upsertProductoRetail: Nueva Laptop '{modelo}' salteada por no tener procesador válido en el título.")
                        return

                elif nombreCategoria == 'CPU':
                    modelo_lower = modelo.lower()
                    console_terms = ["consola", "playstation", "ps5", "ps4", "xbox", "nintendo", "switch", "gamepad", "joystick"]
                    if any(term in modelo_lower for term in console_terms):
                        print(f"// upsertProductoRetail: Nuevo CPU '{modelo}' salteado por ser una consola o periférico.")
                        return
                    cpu_keywords = ['procesador', 'ryzen', 'core i', 'intel core', 'athlon', 'threadripper', 'celeron', 'pentium', 'xeon']
                    if not any(kw in modelo_lower for kw in cpu_keywords):
                        print(f"// upsertProductoRetail: Nuevo CPU '{modelo}' salteado por falta de palabras clave de procesador.")
                        return

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

                # Si es CPU, insertar en la tabla cpu con specs por defecto
                # (los scrapers de AMD/Intel crean CPUs con datos reales via upsertCPU;
                #  esto cubre CPUs de retail que no tuvieron coincidencia)
                elif nombreCategoria == 'CPU':
                    cursor.execute("""
                        INSERT INTO cpu (id_producto, nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (idProducto, 6, 12, 3.0, 4.5, 65))

                # Si es GPU, insertar en la tabla gpu con specs extraídas del título
                elif nombreCategoria == 'GPU':
                    specs = extraer_specs_gpu(modelo)
                    cursor.execute("""
                        INSERT INTO gpu (id_producto, vram, tipo_memoria, consumo_wh)
                        VALUES (%s, %s, %s, %s)
                    """, (idProducto, specs['vram_gb'], specs['tipo_memoria'], specs['tdp_w']))

                # Si es RAM, insertar en la tabla ram con specs extraídas del título
                elif nombreCategoria == 'RAM':
                    specs = extraer_specs_ram(modelo)
                    tipo_ram = specs['tipo_memoria']
                    if tipo_ram not in ['DDR3', 'DDR4', 'DDR5']:
                        tipo_ram = 'DDR4'
                    cursor.execute("""
                        INSERT INTO ram (id_producto, capacidad_gb_ram, velocidad_mhz, latencia_cl, tipo_ram)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (idProducto, specs['capacidad_gb'], specs['velocidad_mhz'], specs['latencia'], tipo_ram))

                # Si es Almacenamiento, insertar en la tabla almacenamiento con specs extraídas
                elif nombreCategoria == 'Almacenamiento':
                    specs = extraer_specs_almacenamiento(modelo)
                    vel_escritura = int(specs['velocidad_lectura'] * 0.8)
                    cursor.execute("""
                        INSERT INTO almacenamiento (id_producto, capacidad_gb_almacenamiento, tipo_almacenamiento, vel_lectura, vel_escritura)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (idProducto, specs['capacidad_gb'], specs['tipo_disco'], specs['velocidad_lectura'], vel_escritura))

            # Insertar o actualizar el precio en la tienda
            if precio > 0:
                if validar_url_retail(urlProducto, nombreTienda):
                    cursor.execute("SELECT id_tienda FROM tiendas WHERE nombre_tienda = %s", (nombreTienda,))
                    tiendaRow = cursor.fetchone()
                    if tiendaRow:
                        cursor.execute("""
                            INSERT INTO producto_tienda (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
                            VALUES (%s, %s, %s, %s, NOW())
                            ON DUPLICATE KEY UPDATE precio = %s, url_producto = %s, fec_actualizacion = NOW()
                        """, (idProducto, tiendaRow['id_tienda'], precio, urlProducto, precio, urlProducto))
                else:
                    print(f"// upsertProductoRetail: Enlace invalido para {nombreTienda}: '{urlProducto}'. Salteando guardado de precio.")

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertProductoRetail: {e}")
        finally:
            cursor.close()

    # upsertCPU - Inserta un procesador o lo saltea si el modelo ya existe.
    def upsertCPU(self, modelo, nucleos, hilos, frecBase, frecTurbo, tdp, urlReferencia):
        modelo_lower = modelo.lower()
        console_terms = ["consola", "playstation", "ps5", "ps4", "xbox", "nintendo", "switch", "gamepad", "joystick"]
        if any(term in modelo_lower for term in console_terms):
            print(f"// upsertCPU: CPU '{modelo}' salteada por ser una consola.")
            return

        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_producto FROM productos WHERE modelo_producto = %s", (modelo,))
            existente = cursor.fetchone()
            if existente:
                # verificarSpecs - Si ya existe el producto, asegurar que tenga registro en la tabla cpu
                idProductoExistente = existente['id_producto']
                cursor.execute("SELECT id_CPU FROM cpu WHERE id_producto = %s", (idProductoExistente,))
                if not cursor.fetchone():
                    # repararHuerfano - Insertamos las specs reales que trae el scraper oficial
                    cursor.execute("""
                        INSERT INTO cpu (id_producto, nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (idProductoExistente, nucleos, hilos, frecBase, frecTurbo, tdp))
                    self.conexion.commit()
                    print(f"// upsertCPU: CPU '{modelo}' (ID: {idProductoExistente}) reparado con specs reales del scraper.")
                return

            nombreMarca = "AMD" if "AMD" in modelo or "Ryzen" in modelo else "Intel"
            marcaObj = MarcaDAO().obtenerMarcaPorId_nombre(nombreMarca)
            if not marcaObj:
                print(f"// upsertCPU: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaObj.idMarca

            categoriaObj = CategoriaDAO().obtenerCategoriaPorNombre('CPU')
            if not categoriaObj:
                return
            idCategoria = categoriaObj.idCategoria

            cursor.execute(
                "INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)",
                (modelo, "", idMarca, idCategoria)
            )
            idProducto = cursor.lastrowid

            cursor.execute("""
                INSERT INTO cpu (id_producto, nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idProducto, nucleos, hilos, frecBase, frecTurbo, tdp))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertCPU: {e}")
        finally:
            cursor.close()

    # upsertGPU - Inserta una placa de video o la saltea si el modelo ya existe.
    def upsertGPU(self, modelo, vramGb, tipoMemoria, busBits, tdpW, imgUrl, urlReferencia):
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_producto FROM productos WHERE modelo_producto = %s", (modelo,))
            existente = cursor.fetchone()
            if existente:
                # verificarSpecs - Si ya existe el producto, asegurar que tenga registro en la tabla gpu
                idProductoExistente = existente['id_producto']
                cursor.execute("SELECT id_GPU FROM gpu WHERE id_producto = %s", (idProductoExistente,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO gpu (id_producto, vram, tipo_memoria, consumo_wh)
                        VALUES (%s, %s, %s, %s)
                    """, (idProductoExistente, vramGb, tipoMemoria, tdpW))
                    self.conexion.commit()
                    print(f"// upsertGPU: GPU '{modelo}' (ID: {idProductoExistente}) reparado con specs reales del scraper.")
                return

            nombreMarca = "NVIDIA" if any(k in modelo for k in ["RTX", "GTX", "GeForce", "NVIDIA"]) else "AMD"
            cursor.execute("SELECT id_marca FROM marcas WHERE nombre_marca = %s", (nombreMarca,))
            marcaRow = cursor.fetchone()
            if not marcaRow:
                print(f"// upsertGPU: marca '{nombreMarca}' no encontrada en BD. Salteando.")
                return
            idMarca = marcaRow['id_marca']

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = 'GPU'")
            categoriaRow = cursor.fetchone()
            if not categoriaRow:
                return
            idCategoria = categoriaRow['id_categoria']

            cursor.execute(
                "INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria) VALUES (%s, %s, %s, %s)",
                (modelo, imgUrl or "", idMarca, idCategoria)
            )
            idProducto = cursor.lastrowid

            cursor.execute("""
                INSERT INTO gpu (id_producto, vram, tipo_memoria, consumo_wh)
                VALUES (%s, %s, %s, %s)
            """, (idProducto, vramGb, tipoMemoria, tdpW))

            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            print(f"// errorUpsertGPU: {e}")
        finally:
            cursor.close()

    # obtenerCPUPorId - Recupera todas las especificaciones de un procesador de la tabla cpu.
    def obtenerCPUPorId(self, idProducto):
        query = """
            SELECT
                p.id_producto, p.modelo_producto, p.img_url, p.id_categoria, p.id_marca,
                c.nombre_categoria as categoria, m.nombre_marca as marca,
                cpu.nucleos, cpu.hilos, cpu.frecuencia_base, cpu.frecuencia_turbo, cpu.tdp
            FROM productos p
            JOIN cpu ON p.id_producto = cpu.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            row = cursor.fetchone()
            if not row:
                return None
            cpu = CPU(
                idProducto=row['id_producto'],
                modeloProducto=row['modelo_producto'],
                imgUrl=row['img_url'],
                urlOficial=None,
                idCategoria=row['id_categoria'],
                idMarca=row['id_marca'],
                nucleos=row['nucleos'],
                hilos=row['hilos'],
                frecuenciaBase=row['frecuencia_base'],
                frecuenciaTurbo=row['frecuencia_turbo'],
                tdp=row['tdp']
            )
            cpu.categoria = row['categoria']
            cpu.marca = row['marca']
            return cpu
        except Exception as e:
            print(f"// errorObtenerCPU: {e}")
            return None
        finally:
            cursor.close()

    # obtenerGPUPorId - Recupera las especificaciones de una placa de video.
    def obtenerGPUPorId(self, idProducto):
        query = """
            SELECT
                p.id_producto, p.modelo_producto, p.img_url, p.id_categoria, p.id_marca,
                c.nombre_categoria as categoria, m.nombre_marca as marca,
                g.id_gpu, g.vram, g.tipo_memoria, g.consumo_wh
            FROM productos p
            JOIN gpu g ON p.id_producto = g.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            row = cursor.fetchone()
            if not row:
                return None
            gpu = GPU(
                idProducto=row['id_producto'],
                modeloProducto=row['modelo_producto'],
                imgUrl=row['img_url'],
                urlOficial=None,
                idCategoria=row['id_categoria'],
                idMarca=row['id_marca'],
                idGPU=row['id_gpu'],
                vram=row['vram'],
                tipoMemoria=row['tipo_memoria'],
                consumoWh=row['consumo_wh']
            )
            gpu.categoria = row['categoria']
            gpu.marca = row['marca']
            return gpu
        except Exception as e:
            print(f"// errorObtenerGPU: {e}")
            return None
        finally:
            cursor.close()

    # obtenerRAMPorId - Recupera las especificaciones de un módulo de memoria RAM.
    def obtenerRAMPorId(self, idProducto):
        query = """
            SELECT
                p.id_producto, p.modelo_producto, p.img_url, p.id_categoria, p.id_marca,
                c.nombre_categoria as categoria, m.nombre_marca as marca,
                r.id_ram, r.capacidad_gb_ram, r.velocidad_mhz, r.latencia_cl, r.tipo_ram
            FROM productos p
            JOIN ram r ON p.id_producto = r.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            row = cursor.fetchone()
            if not row:
                return None
            ram = RAM(
                idProducto=row['id_producto'],
                modeloProducto=row['modelo_producto'],
                imgUrl=row['img_url'],
                urlOficial=None,
                idCategoria=row['id_categoria'],
                idMarca=row['id_marca'],
                idRAM=row['id_ram'],
                capacidadGbRam=row['capacidad_gb_ram'],
                velocidadMhz=row['velocidad_mhz'],
                latenciaCl=row['latencia_cl'],
                tipoRam=row['tipo_ram']
            )
            ram.categoria = row['categoria']
            ram.marca = row['marca']
            return ram
        except Exception as e:
            print(f"// errorObtenerRAM: {e}")
            return None
        finally:
            cursor.close()

    # obtenerAlmacenamientoPorId - Recupera las especificaciones de un disco SSD/HDD.
    def obtenerAlmacenamientoPorId(self, idProducto):
        query = """
            SELECT
                p.id_producto, p.modelo_producto, p.img_url, p.id_categoria, p.id_marca,
                c.nombre_categoria as categoria, m.nombre_marca as marca,
                a.id_almacenamiento, a.capacidad_gb_almacenamiento, a.tipo_almacenamiento,
                a.vel_lectura, a.vel_escritura
            FROM productos p
            JOIN almacenamiento a ON p.id_producto = a.id_producto
            LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
            LEFT JOIN marcas m ON p.id_marca = m.id_marca
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            row = cursor.fetchone()
            if not row:
                return None
            alm = Almacenamiento(
                idProducto=row['id_producto'],
                modeloProducto=row['modelo_producto'],
                imgUrl=row['img_url'],
                urlOficial=None,
                idCategoria=row['id_categoria'],
                idMarca=row['id_marca'],
                idAlmacenamiento=row['id_almacenamiento'],
                capacidadGbAlmacenamiento=row['capacidad_gb_almacenamiento'],
                tipoAlmacenamiento=row['tipo_almacenamiento'],
                velLectura=row['vel_lectura'],
                velEscritura=row['vel_escritura']
            )
            alm.categoria = row['categoria']
            alm.marca = row['marca']
            return alm
        except Exception as e:
            print(f"// errorObtenerAlmacenamiento: {e}")
            return None
        finally:
            cursor.close()

    # obtenerCategoriaPorId - Obtiene el nombre de la categoría del producto.
    def obtenerCategoriaPorId(self, idProducto):
        query = """
            SELECT c.nombre_categoria 
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.id_producto = %s
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            resultado = cursor.fetchone()
            return resultado['nombre_categoria'] if resultado else None
        except Exception as e:
            print(f"// errorObtenerCategoriaPorId: {e}")
            return None
        finally:
            cursor.close()

    # obtenerPreciosProducto - Obtiene la lista de precios y enlaces del producto en tiendas.
    def obtenerPreciosProducto(self, idProducto):
        query = """
            SELECT 
                t.nombre_tienda, 
                s.precio, 
                s.url_producto, 
                s.fec_actualizacion
            FROM producto_tienda s
            JOIN tiendas t ON s.id_tienda = t.id_tienda
            WHERE s.id_producto = %s
            ORDER BY s.precio ASC
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idProducto,))
            return cursor.fetchall()
        except Exception as e:
            print(f"// errorObtenerPreciosProducto: {e}")
            return []
        finally:
            cursor.close()

    # obtenerDetalleProducto - Obtiene el detalle completo de un producto según su categoría.
    # Retorna un dict con los datos generales y las especificaciones técnicas.
    def obtenerDetalleProducto(self, idProducto):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT
                        p.id_producto, p.modelo_producto as modelo, p.img_url,
                        c.nombre_categoria as categoria,
                        m.nombre_marca as marca
                    FROM productos p
                    LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
                    LEFT JOIN marcas m ON p.id_marca = m.id_marca
                    WHERE p.id_producto = %s
                """, (idProducto,))
                producto = cursor.fetchone()
            finally:
                cursor.close()

            if not producto:
                return None

            prod_obj = Producto(
                idProducto=producto['id_producto'],
                modeloProducto=producto['modelo'],
                imgUrl=producto['img_url'],
                urlOficial=None,
                idCategoria=None,
                idMarca=None
            )
            prod_obj.categoria = producto['categoria']
            prod_obj.marca = producto['marca']

            categoria = producto['categoria']
            specs = None

            if categoria == 'Laptop':
                specs = self.obtenerLaptopPorId(idProducto)
            elif categoria == 'CPU':
                specs = self.obtenerCPUPorId(idProducto)
            elif categoria == 'GPU':
                specs = self.obtenerGPUPorId(idProducto)
            elif categoria == 'RAM':
                specs = self.obtenerRAMPorId(idProducto)
            elif categoria == 'Almacenamiento':
                specs = self.obtenerAlmacenamientoPorId(idProducto)

            precios = self.obtenerPreciosProducto(idProducto)

            return {
                'producto': prod_obj,
                'specs': specs,
                'precios': precios
            }

        except Exception as e:
            print(f"// errorObtenerDetalleProducto: {e}")
            return None

    # obtenerIdCategoriaNumerica - Devuelve el id_categoria (entero) de un producto.
    # Usado por el controlador para guardar comparaciones sin abrir cursores en la capa web.
    def obtenerIdCategoriaNumerica(self, idProducto):
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id_categoria FROM productos WHERE id_producto = %s", (idProducto,))
            resultado = cursor.fetchone()
            return resultado['id_categoria'] if resultado else 1
        except Exception as e:
            print(f"// errorObtenerIdCategoriaNumerica: {e}")
            return 1
        finally:
            cursor.close()

    # _repararSpecsSiFaltan - Verifica que un producto tenga su registro en la tabla de specs correspondiente.
    # Si está huérfano (existe en 'productos' pero no en la tabla de specs), inserta valores por defecto.
    # Esto previene errores al comparar productos que fueron importados sin especificaciones.
    def _repararSpecsSiFaltan(self, cursor, idProducto, nombreCategoria, modelo):
        try:
            if nombreCategoria == 'CPU':
                cursor.execute("SELECT id_CPU FROM cpu WHERE id_producto = %s", (idProducto,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO cpu (id_producto, nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp)
                        VALUES (%s, 6, 12, 3.00, 4.50, 65)
                    """, (idProducto,))
                    print(f"// repararSpecs: CPU '{modelo}' (ID: {idProducto}) reparado con specs por defecto.")

            elif nombreCategoria == 'GPU':
                cursor.execute("SELECT id_GPU FROM gpu WHERE id_producto = %s", (idProducto,))
                if not cursor.fetchone():
                    specs = extraer_specs_gpu(modelo)
                    cursor.execute("""
                        INSERT INTO gpu (id_producto, vram, tipo_memoria, consumo_wh)
                        VALUES (%s, %s, %s, %s)
                    """, (idProducto, specs['vram_gb'], specs['tipo_memoria'], specs['tdp_w']))
                    print(f"// repararSpecs: GPU '{modelo}' (ID: {idProducto}) reparado con specs por defecto.")

            elif nombreCategoria == 'RAM':
                cursor.execute("SELECT id_RAM FROM ram WHERE id_producto = %s", (idProducto,))
                if not cursor.fetchone():
                    specs = extraer_specs_ram(modelo)
                    tipo_ram = specs['tipo_memoria']
                    if tipo_ram not in ['DDR3', 'DDR4', 'DDR5']:
                        tipo_ram = 'DDR4'
                    cursor.execute("""
                        INSERT INTO ram (id_producto, capacidad_gb_ram, velocidad_mhz, latencia_cl, tipo_ram)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (idProducto, specs['capacidad_gb'], specs['velocidad_mhz'], specs['latencia'], tipo_ram))
                    print(f"// repararSpecs: RAM '{modelo}' (ID: {idProducto}) reparado con specs por defecto.")

            elif nombreCategoria == 'Almacenamiento':
                cursor.execute("SELECT id_almacenamiento FROM almacenamiento WHERE id_producto = %s", (idProducto,))
                if not cursor.fetchone():
                    specs = extraer_specs_almacenamiento(modelo)
                    vel_escritura = int(specs['velocidad_lectura'] * 0.8)
                    cursor.execute("""
                        INSERT INTO almacenamiento (id_producto, capacidad_gb_almacenamiento, tipo_almacenamiento, vel_lectura, vel_escritura)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (idProducto, specs['capacidad_gb'], specs['tipo_disco'], specs['velocidad_lectura'], vel_escritura))
                    print(f"// repararSpecs: Almacenamiento '{modelo}' (ID: {idProducto}) reparado con specs por defecto.")

        except Exception as e:
            print(f"// errorRepararSpecs: {e} — Producto: {modelo} (ID: {idProducto})")
