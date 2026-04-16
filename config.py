"""
config.py
---------
Configuración centralizada de la aplicación.
Si después querés ocultar credenciales, se pasan a un archivo .env.
"""


class Config:
    # --- Base de datos (Laragon por defecto usa root sin contraseña) ---
    DB_HOST = "127.0.0.1"
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = ""          # dejar vacío si Laragon no te pidió una
    DB_NAME = "techmatch"

    # --- Flask ---
    # En producción esto DEBE venir de una variable de entorno.
    SECRET_KEY = "cambiar-esta-clave-en-produccion-techmatch-2026"