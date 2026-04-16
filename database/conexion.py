"""
conexion.py
-----------
Clase `ConexionDB` - encargada de abrir conexiones a MySQL.

Implementa el patrón Singleton: una única instancia vive en memoria
para no crear múltiples pools ni desperdiciar recursos.
"""

import mysql.connector
from mysql.connector import Error
from config import Config


class ConexionDB:
    _instancia = None  # guardamos acá la única instancia permitida

    def __new__(cls):
        # Si todavía no existe, la creamos. Si ya existe, devolvemos esa.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def obtener_conexion(self):
        """Devuelve una conexión nueva a MySQL. El caller la cierra."""
        try:
            return mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
            )
        except Error as e:
            print(f"[ConexionDB] ERROR al conectar: {e}")
            raise