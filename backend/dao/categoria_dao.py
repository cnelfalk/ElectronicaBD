import mysql.connector
from database.conexion import ConexionDB

class CategoriaDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no, inicializa el Singleton global de TechMatch usando obtenerInstancia().
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def obtenerCategorias(self):
        """Devuelve el listado completo de categorías registradas en el sistema (ej: Laptop, CPU)."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_categoria, nombre_categoria FROM categorias ORDER BY nombre_categoria ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [CategoriaDAO] Error al obtener categorías: {err}")
            return []
        finally:
            cursor.close()

    def obtenerCategoriaPorId(self, id_categoria):
        """Busca y devuelve una categoría específica por su ID primario."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_categoria, nombre_categoria FROM categorias WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"// [CategoriaDAO] Error al buscar categoría {id_categoria}: {err}")
            return None
        finally:
            cursor.close()

    def guardarCategoria(self, nombre_categoria):
        """Inserta una nueva categoría en el maestro."""
        cursor = self.conexion.cursor()
        try:
            sql = "INSERT IGNORE INTO categorias (nombre_categoria) VALUES (%s)"
            cursor.execute(sql, (nombre_categoria,))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [CategoriaDAO] Error al guardar categoría {nombre_categoria}: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()