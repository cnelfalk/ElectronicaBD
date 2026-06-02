import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE modelo_producto LIKE '%Beast%' OR modelo_producto LIKE '%Kingston%'")
    rows = cursor.fetchall()
    print("Found products matching 'Beast' or 'Kingston':")
    for r in rows:
        print(r)
    cursor.close()
