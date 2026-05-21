import mysql.connector
# Importamos tu clase de conexión
from database.conexion import ConexionDB

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
            sql = "SELECT id_marca, nombre_marca FROM marcas ORDER BY nombre_marca ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al obtener marcas: {err}")
            return []
        finally:
            cursor.close()

    def obtenerMarcaPorId(self, id_marca):
        """Busca y devuelve una marca específica por su ID primario."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT id_marca, nombre_marca FROM marcas WHERE id_marca = %s"
            cursor.execute(sql, (id_marca,))
            return cursor.fetchone()
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al buscar marca {id_marca}: {err}")
            return None
        finally:
            cursor.close()

    def guardarMarca(self, nombre_marca):
        """Inserta una nueva marca en el maestro evitando duplicados por nombre."""
        cursor = self.conexion.cursor()
        try:
            sql = "INSERT IGNORE INTO marcas (nombre_marca) VALUES (%s)"
            cursor.execute(sql, (nombre_marca,))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [MarcaDAO] Error al guardar marca {nombre_marca}: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()