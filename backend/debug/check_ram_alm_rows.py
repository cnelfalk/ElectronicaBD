import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn:
    cursor = conn.cursor(dictionary=True)
    
    # Count rows in ram and almacenamiento
    for table in ['ram', 'almacenamiento', 'gpu']:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        print(f"Table {table} has {cursor.fetchone()['count']} rows")
        
    # Get products by category
    cursor.execute("""
        SELECT c.nombre_categoria, COUNT(p.id_producto) as count 
        FROM productos p 
        JOIN categorias c ON p.id_categoria = c.id_categoria 
        GROUP BY c.nombre_categoria
    """)
    print("\nProducts count by category:")
    for row in cursor.fetchall():
        print(f"Category {row['nombre_categoria']}: {row['count']} products")
        
    # Get list of RAM products and check if they have specs
    cursor.execute("""
        SELECT p.id_producto, p.modelo_producto, r.id_ram 
        FROM productos p 
        LEFT JOIN ram r ON p.id_producto = r.id_producto 
        WHERE p.id_categoria = (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'RAM')
    """)
    print("\nRAM products in DB:")
    for row in cursor.fetchall():
        print(f"ID: {row['id_producto']} | Model: {row['modelo_producto'][:50]} | RAM ID: {row['id_ram']}")

    # Get list of Almacenamiento products and check if they have specs
    cursor.execute("""
        SELECT p.id_producto, p.modelo_producto, a.id_almacenamiento 
        FROM productos p 
        LEFT JOIN almacenamiento a ON p.id_producto = a.id_producto 
        WHERE p.id_categoria = (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'Almacenamiento')
    """)
    print("\nAlmacenamiento products in DB:")
    for row in cursor.fetchall():
        print(f"ID: {row['id_producto']} | Model: {row['modelo_producto'][:50]} | Storage ID: {row['id_almacenamiento']}")

    # Get list of GPU products and check if they have specs
    cursor.execute("""
        SELECT p.id_producto, p.modelo_producto, g.id_GPU 
        FROM productos p 
        LEFT JOIN gpu g ON p.id_producto = g.id_producto 
        WHERE p.id_categoria = (SELECT id_categoria FROM categorias WHERE nombre_categoria = 'GPU')
    """)
    print("\nGPU products in DB:")
    for row in cursor.fetchall():
        print(f"ID: {row['id_producto']} | Model: {row['modelo_producto'][:50]} | GPU ID: {row['id_GPU']}")

    cursor.close()
