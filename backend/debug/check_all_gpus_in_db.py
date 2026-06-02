import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, modelo_producto FROM productos WHERE id_categoria = 3")
    rows = cursor.fetchall()
    print("ALL GPUs in productos table:")
    for r in rows:
        print(f"ID: {r['id_producto']} | Model: {r['modelo_producto']}")
    cursor.close()
