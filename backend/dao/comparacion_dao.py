import mysql.connector
from database.conexion import ConexionDB

class ComparacionDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no se le pasa ninguna (como en producción), inicializa y usa el Singleton global.
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def guardarComparacion(self, id_usuario, id_producto_a, id_producto_b, id_categoria=1):
        """
        Guarda una comparación aprovechando el AUTO_INCREMENT de la base de datos.
        Inserta en cascada en las tablas cabecera (comparaciones_guardadas) y detalle (contiene).
        """
        cursor = self.conexion.cursor()
        try:
            # 1. Insertamos la cabecera (MySQL genera el id_comparacion solo por AUTO_INCREMENT)
            sql_cabecera = """
                INSERT INTO comparaciones_guardadas (fec_creacion_comp, id_categoria, id_usuario) 
                VALUES (NOW(), %s, %s)
            """
            cursor.execute(sql_cabecera, (id_categoria, id_usuario))
            
            # 2. Capturamos el ID autogenerado inmediatamente
            id_comparacion = cursor.lastrowid

            # 3. Insertamos las dos filas de detalle en la tabla 'contiene'
            sql_detalle = """
                INSERT IGNORE INTO contiene (id_producto, id_comparacion) 
                VALUES (%s, %s)
            """
            # Producto A
            cursor.execute(sql_detalle, (id_producto_a, id_comparacion))
            # Producto B
            cursor.execute(sql_detalle, (id_producto_b, id_comparacion))

            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al guardar con AUTO_INCREMENT: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def eliminarComparacion(self, id_comparacion):
        """Elimina una comparación limpiando primero el detalle y luego la cabecera."""
        cursor = self.conexion.cursor()
        try:
            # 1. Eliminar del detalle por clave foránea
            cursor.execute("DELETE FROM contiene WHERE id_comparacion = %s", (id_comparacion,))
            
            # 2. Eliminar la cabecera
            cursor.execute("DELETE FROM comparaciones_guardadas WHERE id_comparacion = %s", (id_comparacion,))
            
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al eliminar: {err}")
            self.conexion.rollback()
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
                    GROUP_CONCAT(p.id_producto ORDER BY p.id_producto) as ids_productos,
                    GROUP_CONCAT(p.modelo_producto SEPARATOR ' vs ') as duplas_modelos
                FROM comparaciones_guardadas cg
                JOIN contiene c ON cg.id_comparacion = c.id_comparacion
                JOIN productos p ON c.id_producto = p.id_producto
                WHERE cg.id_usuario = %s
                GROUP BY cg.id_comparacion
                ORDER BY cg.fec_creacion_comp DESC
            """
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al listar: {err}")
            return []
        finally:
            cursor.close()