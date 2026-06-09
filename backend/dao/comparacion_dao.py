import mysql.connector
from database.conexion import ConexionDB

from modelos.comparacion_guardada import ComparacionGuardada

class ComparacionDAO:
    @property
    def conexion(self):
        return ConexionDB.obtenerInstancia()

    def guardarComparacion(self, id_usuario, id_producto_a, id_producto_b, id_categoria=1):
        """
        Guarda una comparación insertando la cabecera (comparaciones_guardadas) y el detalle (producto_comparacion)
        de forma atómica en la base de datos usando consultas SQL directas y una transacción.
        """
        cursor = self.conexion.cursor()
        try:
            # 1. Insertar cabecera — MySQL genera el id por AUTO_INCREMENT
            sql_cabecera = """
                INSERT INTO comparaciones_guardadas (fec_creacion_comp, id_categoria, id_usuario)
                VALUES (NOW(), %s, %s)
            """
            cursor.execute(sql_cabecera, (id_categoria, id_usuario))
            
            # 2. Capturar el ID recién generado con LAST_INSERT_ID()
            cursor.execute("SELECT LAST_INSERT_ID()")
            v_id_comparacion = cursor.fetchone()[0]
            
            # 3. Insertar los dos productos en la tabla de detalle
            sql_detalle = """
                INSERT IGNORE INTO producto_comparacion (id_producto, id_comparacion)
                VALUES (%s, %s)
            """
            cursor.execute(sql_detalle, (id_producto_a, v_id_comparacion))
            cursor.execute(sql_detalle, (id_producto_b, v_id_comparacion))
            
            self.conexion.commit()
            return True, None
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al guardar comparación: {err}")
            self.conexion.rollback()
            return False, str(err)
        finally:
            cursor.close()

    def eliminarComparacion(self, id_comparacion):
        """Elimina una comparación borrando el detalle y la cabecera con consultas SQL directas."""
        cursor = self.conexion.cursor()
        try:
            # 1. Borrar el detalle (tabla hija) para respetar la clave foránea
            sql_detalle = "DELETE FROM producto_comparacion WHERE id_comparacion = %s"
            cursor.execute(sql_detalle, (id_comparacion,))

            # 2. Borrar la cabecera
            sql_cabecera = "DELETE FROM comparaciones_guardadas WHERE id_comparacion = %s"
            cursor.execute(sql_cabecera, (id_comparacion,))

            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al eliminar comparación: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def existeComparacion(self, id_usuario, id_producto_a, id_producto_b):
        """Devuelve True si el usuario ya tiene guardada una comparación con exactamente esos dos productos."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = """
                SELECT cg.id_comparacion
                FROM comparaciones_guardadas cg
                WHERE cg.id_usuario = %s
                  AND (SELECT COUNT(*) FROM producto_comparacion c WHERE c.id_comparacion = cg.id_comparacion) = 2
                  AND EXISTS (SELECT 1 FROM producto_comparacion c WHERE c.id_comparacion = cg.id_comparacion AND c.id_producto = %s)
                  AND EXISTS (SELECT 1 FROM producto_comparacion c WHERE c.id_comparacion = cg.id_comparacion AND c.id_producto = %s)
                LIMIT 1
            """
            cursor.execute(sql, (id_usuario, id_producto_a, id_producto_b))
            return cursor.fetchone() is not None
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al verificar duplicado: {err}")
            return False
        finally:
            cursor.close()

    def obtenerComparacionesUsuario(self, id_usuario):
        """Trae el historial agrupando los productos usando GROUP_CONCAT."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = """
                SELECT 
                    cg.id_comparacion,
                    cg.fec_creacion_comp as fecha,
                    cat.nombre_categoria as categoria,
                    GROUP_CONCAT(p.id_producto ORDER BY p.id_producto) as ids_productos,
                    GROUP_CONCAT(p.modelo_producto SEPARATOR ' vs ') as duplas_modelos
                FROM comparaciones_guardadas cg
                JOIN producto_comparacion c ON cg.id_comparacion = c.id_comparacion
                JOIN productos p ON c.id_producto = p.id_producto
                JOIN categorias cat ON cg.id_categoria = cat.id_categoria
                WHERE cg.id_usuario = %s
                GROUP BY cg.id_comparacion, cat.nombre_categoria
                ORDER BY cg.fec_creacion_comp DESC
            """
            cursor.execute(sql, (id_usuario,))
            rows = cursor.fetchall()
            comparaciones = []
            for row in rows:
                cg = ComparacionGuardada(
                    idComparacion=row['id_comparacion'],
                    fecCreacionComp=row['fecha'],
                    idCategoria=row['categoria'],
                    idUsuario=id_usuario,
                    productos=[]
                )
                cg.ids_productos = row['ids_productos']
                cg.duplas_modelos = row['duplas_modelos']
                comparaciones.append(cg)
            return comparaciones
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al listar: {err}")
            return []
        finally:
            cursor.close()