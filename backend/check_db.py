import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn is None:
    print("No connection could be established!")
else:
    print("Connection successful!")
    cursor = conn.cursor()
    tables = ['marcas', 'categorias', 'tiendas', 'socket', 'productos', 'cpu', 'gpu', 'laptops', 'producto_tienda']
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cursor.fetchone()[0]
            print(f"Table {t}: {cnt} rows")
        except Exception as e:
            print(f"Error on {t}: {e}")
    
    # Check if there is data in auxiliary tables
    for t in ['marcas', 'categorias', 'tiendas', 'socket']:
        try:
            cursor.execute(f"SELECT * FROM {t} LIMIT 5")
            rows = cursor.fetchall()
            print(f"\n--- {t} ---")
            for r in rows:
                print(r)
        except Exception as e:
            print(f"Error reading {t}: {e}")
    cursor.close()
