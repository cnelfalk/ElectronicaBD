import mysql.connector
from mysql.connector import Error
from config import Config

# // ClaseConexionDB - gestiona la conexion unica a la base de datos MySQL
class ConexionDB:
    _instancia = None

    def __init__(self):
        # // ValidarInstancia - evita la creacion de nuevas instancias manuales
        if ConexionDB._instancia is not None:
            raise Exception("Esta clase es un Singleton. Usa obtenerInstancia()")

    @classmethod
    def obtenerInstancia(cls):
        if cls._instancia is None:
            try:
                # Configuracion centralizada hacia la IP de Tailscale
                cls._instancia = mysql.connector.connect(
                    host="127.0.0.1",    
                    user="fabrizio_tm",     
                    password="admin",     
                    database="techmatch",
                    port=3306
                )
                print("// Conexión establecida con el servidor central de BD")
            except Exception as e:
                print(f"// Error crítico de conexión a la BD central: {e}")
        return cls._instancia

    @staticmethod
    # // _conectar - realiza la apertura del canal de datos con el servidor
    def _conectar():
        try:
            conexion = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"// errorConexion: {e}")
            return None