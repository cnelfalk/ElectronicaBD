import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as count FROM ram")
    print(f"Current rows in ram table: {cursor.fetchone()['count']}")
    
    cursor.execute("SELECT COUNT(*) as count FROM productos WHERE id_categoria = 4")
    print(f"Current products in RAM category: {cursor.fetchone()['count']}")
    cursor.close()
