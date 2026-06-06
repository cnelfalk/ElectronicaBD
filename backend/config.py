import os

# // ClaseConfiguracion - centraliza los parametros del sistema
class Config:
    # // ClaveSecreta - utilizada para la seguridad de tokens y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'techmatch_secret_key_2026'
    
    # // ConfiguracionBaseDeDatos - parametros para la conexion a MySQL en Laragon
    DB_HOST = os.environ.get('DB_HOST') or '100.82.23.52'
    DB_USER = 'fabrizio_tm'
    DB_PASSWORD = 'admin'
    DB_NAME = 'techmatch'

    # // ConfiguracionSMTP - parametros para el envío de emails de recuperación vía Gmail
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL') or 'techmatch.noreply@gmail.com'
    
    # ¡ACÁ REEMPLAZÁS EL TEXTO POR LA CONTRASEÑA DE APLICACIÓN DE GOOGLE!
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or 'okas fjst ucsh jskd'