import mysql.connector
from database.conexion import ConexionDB

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
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [TiendaDAO] Error al obtener tiendas: {err}")
            return []
        finally:
            cursor.close()

    def obtenerTiendaPorId(self, id_tienda):
        """Busca y devuelve una tienda específica por su ID primario."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_tienda, nombre_tienda, url_tienda FROM tiendas WHERE id_tienda = %s"
            cursor.execute(sql, (id_tienda,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"// [TiendaDAO] Error al buscar tienda {id_tienda}: {err}")
            return None
        finally:
            cursor.close()

    def guardarTienda(self, nombre_tienda, url_tienda=None):
        """Inserta una nueva tienda en el catálogo evitando duplicados por nombre."""
        cursor = self.conexion.cursor()
        try:
            sql = "INSERT IGNORE INTO tiendas (nombre_tienda, url_tienda) VALUES (%s, %s)"
            cursor.execute(sql, (nombre_tienda, url_tienda))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [TiendaDAO] Error al guardar tienda {nombre_tienda}: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()
