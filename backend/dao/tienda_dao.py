import mysql.connector
from database.conexion import ConexionDB
from modelos.tienda import Tienda

class TiendaDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no, inicializa el Singleton global de TechMatch usando obtenerInstancia().
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def obtenerTiendas(self):
        """Devuelve el listado completo de tiendas registradas en el sistema."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_tienda, nombre_tienda, url_tienda FROM tiendas ORDER BY nombre_tienda ASC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [Tienda(r['id_tienda'], r['nombre_tienda'], r.get('url_tienda')) for r in rows]
        except mysql.connector.Error as err:
            print(f"// [TiendaDAO] Error al obtener tiendas: {err}")
            return []
        finally:
            cursor.close()


    def obtenerTiendaPorNombre(self, nombre_tienda):
        """Busca y devuelve una tienda específica por su nombre."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_tienda, nombre_tienda, url_tienda FROM tiendas WHERE nombre_tienda = %s"
            cursor.execute(sql, (nombre_tienda,))
            row = cursor.fetchone()
            return Tienda(row['id_tienda'], row['nombre_tienda'], row.get('url_tienda')) if row else None
        except mysql.connector.Error as err:
            print(f"// [TiendaDAO] Error al buscar tienda '{nombre_tienda}': {err}")
            return None
        finally:
            cursor.close()

