import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor()
    for table in ['ram', 'almacenamiento', 'gpu']:
        try:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            print(f"\nColumns for table: {table}")
            for col in columns:
                print(col)
        except Exception as e:
            print(f"Error describing {table}: {e}")
    cursor.close()
