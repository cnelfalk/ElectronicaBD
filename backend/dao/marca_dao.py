import mysql.connector
from database.conexion import ConexionDB
from modelos.marca import Marca

class MarcaDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no, inicializa el Singleton global de TechMatch usando obtenerInstancia().
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def obtenerMarcas(self):
        """Devuelve el listado completo de marcas registradas en el sistema."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_marca, nombre_marca, url_marca FROM marcas ORDER BY nombre_marca ASC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Marca(r['id_marca'], r['nombre_marca'], r.get('url_marca')) for r in rows]
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al obtener marcas: {err}")
            return []
        finally:
            cursor.close()

    def obtenerMarcasConProductos(self):
        """Devuelve solo las marcas que tienen al menos un producto en el catálogo."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = """
                SELECT DISTINCT m.id_marca, m.nombre_marca, m.url_marca
                FROM marcas m
                JOIN productos p ON m.id_marca = p.id_marca
                ORDER BY m.nombre_marca ASC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Marca(r['id_marca'], r['nombre_marca'], r.get('url_marca')) for r in rows]
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al obtener marcas con productos: {err}")
            return []
        finally:
            cursor.close()

    def obtenerMarcaPorId_nombre(self, nombre_marca):
        """Busca y devuelve una marca por su nombre."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_marca, nombre_marca, url_marca FROM marcas WHERE nombre_marca = %s"
            cursor.execute(sql, (nombre_marca,))
            row = cursor.fetchone()
            return Marca(row['id_marca'], row['nombre_marca'], row.get('url_marca')) if row else None
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al buscar marca '{nombre_marca}': {err}")
            return None
        finally:
            cursor.close()

