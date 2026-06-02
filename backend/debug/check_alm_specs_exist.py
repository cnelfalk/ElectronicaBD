import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_almacenamiento, a.id_producto, p.modelo_producto, a.capacidad_gb_almacenamiento as capacidad_gb, a.tipo_almacenamiento as tipo_disco, a.vel_lectura
        FROM almacenamiento a
        JOIN productos p ON a.id_producto = p.id_producto
    """)
    rows = cursor.fetchall()
    print("ALL entries in almacenamiento table:")
    for r in rows:
        print(r)
    cursor.close()
