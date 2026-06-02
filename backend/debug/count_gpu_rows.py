import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM gpu")
    print(f"Current rows in gpu table: {cursor.fetchone()['count']}")
    
    cursor.execute("SELECT COUNT(*) as count FROM productos WHERE id_categoria = 3")
    print(f"Current products in GPU category: {cursor.fetchone()['count']}")
    cursor.close()
