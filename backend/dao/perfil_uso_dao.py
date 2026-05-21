import mysql.connector
from database.conexion import ConexionDB

class PerfilDAO:
    def __init__(self, conexion=None):
        """
        Constructor del DAO. Si se le pasa una conexión activa, la usa.
        Si no, inicializa el Singleton global de TechMatch.
        """
        if conexion:
            self.conexion = conexion
        else:
            self.conexion = ConexionDB.obtenerInstancia()

    def obtenerPerfiles(self):
        """Devuelve todos los perfiles de uso disponibles (Gaming, Ofimática, etc.)."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            # Consulta limpia alineada al 100% con tu esquema de base de datos
            sql = "SELECT id_perfil, nombre_perfil FROM perfiles_uso"
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [PerfilDAO] Error al obtener perfiles: {err}")
            return []
        finally:
            cursor.close()

    def asociarProductoAPerfil(self, id_producto, id_perfil):
        """Asocia un producto a un perfil de uso específico en la tabla productos_perfiles."""
        cursor = self.conexion.cursor()
        try:
            sql = "INSERT IGNORE INTO productos_perfiles (id_producto, id_perfil) VALUES (%s, %s)"
            cursor.execute(sql, (id_producto, id_perfil))
            self.conexion.commit()
            return True
        except mysql.connector.Error as err:
            print(f"// [PerfilDAO] Error al asociar producto a perfil: {err}")
            self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def obtenerProductosPorPerfil(self, nombre_perfil):
        """Trae todos los productos básicos que aplican a un perfil determinado (ej: 'gaming')."""
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = """
                SELECT p.id_producto, p.modelo_producto as modelo, p.img_url, m.nombre_marca as marca
                FROM productos p
                JOIN productos_perfiles pp ON p.id_producto = pp.id_producto
                JOIN perfiles_uso pu ON pp.id_perfil = pu.id_perfil
                LEFT JOIN marcas m ON p.id_marca = m.id_marca
                WHERE pu.nombre_perfil = %s
            """
            cursor.execute(sql, (nombre_perfil,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"// [PerfilDAO] Error al listar productos por perfil: {err}")
            return []
        finally:
            cursor.close()

