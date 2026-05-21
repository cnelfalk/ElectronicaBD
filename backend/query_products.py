import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn is None:
    print("No database connection available!")
    sys.exit(1)

cursor = conn.cursor(dictionary=True)

try:
    cursor.execute("""
        SELECT p.id_producto, p.modelo_producto, m.nombre_marca, c.nombre_categoria,
               l.id_laptop, l.cpu_modelo, l.ram_gb, l.almacenamiento_gb,
               s.precio, t.nombre_tienda
        FROM productos p
        LEFT JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        LEFT JOIN laptops l ON p.id_producto = l.id_producto
        LEFT JOIN se_vende_en s ON p.id_producto = s.id_producto
        LEFT JOIN tiendas t ON s.id_tienda = t.id_tienda
        ORDER BY p.id_producto
    """)
    rows = cursor.fetchall()
    print(f"Total products found in query: {len(rows)}")
    for r in rows[:15]:
        print(f"ID: {r['id_producto']} | Model: {r['modelo_producto'][:40]} | Brand: {r['nombre_marca']} | Cat: {r['nombre_categoria']}")
        print(f"  Laptop Rec: {'Yes' if r['id_laptop'] else 'No'} | CPU: {r['cpu_modelo']} | RAM: {r['ram_gb']}GB | SSD: {r['almacenamiento_gb']}GB")
        print(f"  Sell Rec: {'Yes' if r['precio'] else 'No'} | Price: {r['precio']} | Store: {r['nombre_tienda']}")
        print("-" * 50)
except Exception as e:
    print(f"Error querying products: {e}")
finally:
    cursor.close()
