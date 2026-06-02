import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT g.id_gpu, g.id_producto, p.modelo_producto 
        FROM gpu g 
        JOIN productos p ON g.id_producto = p.id_producto
    """)
    rows = cursor.fetchall()
    print("ALL entries in gpu table:")
    for r in rows:
        print(r)
    cursor.close()
