import mysql.connector
from database.conexion import ConexionDB
from modelos.categoria import Categoria

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
            rows = cursor.fetchall()
            return [Categoria(r['id_categoria'], r['nombre_categoria']) for r in rows]
        except mysql.connector.Error as err:
            print(f"// [CategoriaDAO] Error al obtener categorías: {err}")
            return []
        finally:
            cursor.close()

    def obtenerCategoriaPorNombre(self, nombre_categoria):
        """Busca y devuelve una categoría por su nombre."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_categoria, nombre_categoria FROM categorias WHERE nombre_categoria = %s"
            cursor.execute(sql, (nombre_categoria,))
            row = cursor.fetchone()
            return Categoria(row['id_categoria'], row['nombre_categoria']) if row else None
        except mysql.connector.Error as err:
            print(f"// [CategoriaDAO] Error al buscar categoría '{nombre_categoria}': {err}")
            return None
        finally:
            cursor.close()

