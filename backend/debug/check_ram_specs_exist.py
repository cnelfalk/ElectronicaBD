import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ram WHERE id_producto IN (255, 256)")
    rows = cursor.fetchall()
    print("Found RAM specs for 255, 256:")
    for r in rows:
        print(r)
    cursor.close()
