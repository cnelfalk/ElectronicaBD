import mysql.connector
from database.conexion import ConexionDB

class SocketDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no, inicializa el Singleton global de TechMatch usando obtenerInstancia().
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def obtenerSockets(self):
        """Devuelve el listado completo de sockets registrados (ej: AM4, AM5, LGA1700)."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_socket, nombre_socket FROM socket ORDER BY nombre_socket ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [SocketDAO] Error al obtener sockets: {err}")
            return []
        finally:
            cursor.close()

    def obtenerSocketPorId(self, id_socket):
        """Busca y devuelve un socket específico por su ID primario."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_socket, nombre_socket FROM socket WHERE id_socket = %s"
            cursor.execute(sql, (id_socket,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"// [SocketDAO] Error al buscar socket {id_socket}: {err}")
            return None
        finally:
            cursor.close()

    def guardarSocket(self, nombre_socket):
        """Inserta un nuevo socket en el maestro evitando duplicados por nombre."""
        cursor = self.conexion.cursor()
        try:
            sql = "INSERT IGNORE INTO socket (nombre_socket) VALUES (%s)"
            cursor.execute(sql, (nombre_socket,))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [SocketDAO] Error al guardar socket {nombre_socket}: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()