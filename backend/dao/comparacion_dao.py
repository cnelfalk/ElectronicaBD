import mysql.connector
from database.conexion import ConexionDB

from modelos.comparacion_guardada import ComparacionGuardada

class ComparacionDAO:
    @property
    def conexion(self):
        return ConexionDB.obtenerInstancia()

    def guardarComparacion(self, id_usuario, id_producto_a, id_producto_b, id_categoria=1):
        """
        Guarda una comparación llamando al stored procedure sp_guardar_comparacion.
        El SP inserta la cabecera (comparaciones_guardadas) y el detalle (contiene)
        de forma atómica dentro de MySQL, evitando estados intermedios inconsistentes.
        """
        cursor = self.conexion.cursor()
        try:
            cursor.callproc('sp_guardar_comparacion', [
                id_usuario,
                id_producto_a,
                id_producto_b,
                id_categoria
            ])
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al guardar comparación: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def eliminarComparacion(self, id_comparacion):
        """Elimina una comparación llamando al stored procedure sp_eliminar_comparacion."""
        cursor = self.conexion.cursor()
        try:
            cursor.callproc('sp_eliminar_comparacion', [id_comparacion])
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [ComparacionDAO] Error al llamar sp_eliminar_comparacion: {err}")
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
                  AND (SELECT COUNT(*) FROM contiene c WHERE c.id_comparacion = cg.id_comparacion) = 2
                  AND EXISTS (SELECT 1 FROM contiene c WHERE c.id_comparacion = cg.id_comparacion AND c.id_producto = %s)
                  AND EXISTS (SELECT 1 FROM contiene c WHERE c.id_comparacion = cg.id_comparacion AND c.id_producto = %s)
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
                JOIN contiene c ON cg.id_comparacion = c.id_comparacion
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