import threading
import mysql.connector
from mysql.connector import Error
from config import Config

# ConexionDB - una conexión MySQL por hilo (thread-local).
# Evita conflictos cuando Flask atiende múltiples requests simultáneos en threads distintos.
class ConexionDB:
    _local = threading.local()

    @classmethod
    def obtenerInstancia(cls):
        conexion = getattr(cls._local, 'conexion', None)

        if conexion is None or not conexion.is_connected():
            try:
                conn = mysql.connector.connect(
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    port=3306,
                    connection_timeout=15
                )
                # Forzar cursores buferizados por defecto para evitar "Unread result found"
                orig_cursor = conn.cursor
                conn.cursor = lambda *a, **kw: orig_cursor(*a, **{**kw, 'buffered': True})
                cls._local.conexion = conn
                print("// Conexión establecida con el servidor central de BD")
            except Exception as e:
                print(f"// Error crítico de conexión a la BD central: {e}")
                cls._local.conexion = None
        else:
            # Verificar con ping que la conexión siga activa (is_connected puede mentir tras timeout)
            try:
                cls._local.conexion.ping(reconnect=True, attempts=3, delay=1)
            except Exception as e:
                print(f"// Reconectando a la BD: {e}")
                cls._local.conexion = None
                return cls.obtenerInstancia()

        return cls._local.conexion

