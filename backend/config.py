import os

# // ClaseConfiguracion - centraliza los parametros del sistema
class Config:
    # // ClaveSecreta - utilizada para la seguridad de tokens y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'techmatch_secret_key_2026'
    
    # // ConfiguracionBaseDeDatos - parametros para la conexion a MySQL en Laragon
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'techmatch'