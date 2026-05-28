import os

# // ClaseConfiguracion - centraliza los parametros del sistema
class Config:
    # // ClaveSecreta - utilizada para la seguridad de tokens y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'techmatch_secret_key_2026'
    
    # // ConfiguracionBaseDeDatos - parametros para la conexion a MySQL en Laragon
    DB_HOST = '127.0.0.1'
    DB_USER = 'fabrizio_tm'
    DB_PASSWORD = 'admin'
    DB_NAME = 'techmatch'