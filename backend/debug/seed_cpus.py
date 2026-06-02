import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

conn = ConexionDB.obtenerInstancia()
if conn is None:
    print("No database connection available!")
    sys.exit(1)

cursor = conn.cursor()

try:
    # CPUs to seed: (modelo, brand_id, cores, threads, base_f, turbo_f, tdp, socket_id, cg_price, ml_price)
    cpus = [
        ("AMD Ryzen 5 5600X", 3, 6, 12, 3.7, 4.6, 65, 2, 180000.00, 195000.00),
        ("AMD Ryzen 7 5700X", 3, 8, 16, 3.4, 4.6, 65, 2, 240000.00, 260000.00),
        ("Intel Core i5-12400F", 4, 6, 12, 2.5, 4.4, 65, 4, 175000.00, 190000.00),
        ("Intel Core i7-12700K", 4, 12, 20, 3.6, 5.0, 125, 4, 380000.00, 410000.00)
    ]

    for model, brand, cores, threads, base, turbo, tdp, socket, cg_p, ml_p in cpus:
        # Check if already exists
        cursor.execute("SELECT id_producto FROM productos WHERE modelo_producto = %s", (model,))
        row = cursor.fetchone()
        if row:
            id_prod = row[0]
            print(f"CPU {model} already exists in products (ID {id_prod}). Skipping insertion.")
        else:
            # Insert product
            cursor.execute("""
                INSERT INTO productos (modelo_producto, img_url, id_marca, id_categoria)
                VALUES (%s, %s, %s, 2)
            """, (model, "", brand))
            id_prod = cursor.lastrowid
            
            # Insert CPU specs
            cursor.execute("""
                INSERT INTO cpu (nucleos, hilos, frecuencia_base, frecuencia_turbo, tdp, id_socket, id_producto)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (cores, threads, base, turbo, tdp, socket, id_prod))
            print(f"Inserted CPU: {model} (ID {id_prod})")
        
        # Seed prices
        # Store 1: Mercado Libre, Store 2: Compra Gamer
        cursor.execute("""
            INSERT INTO se_vende_en (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
            VALUES (%s, 1, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE precio = VALUES(precio), fec_actualizacion = NOW()
        """, (id_prod, ml_p, f"https://www.mercadolibre.com.ar/search?as_word={model.replace(' ', '+')}"))
        
        cursor.execute("""
            INSERT INTO se_vende_en (id_producto, id_tienda, precio, url_producto, fec_actualizacion)
            VALUES (%s, 2, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE precio = VALUES(precio), fec_actualizacion = NOW()
        """, (id_prod, cg_p, f"https://www.compragamer.com/?seccion=3&criterio={model.replace(' ', '+')}"))

    conn.commit()
    print("All CPUs and pricing seeded successfully!")
except Exception as e:
    conn.rollback()
    print(f"Error seeding CPUs: {e}")
finally:
    cursor.close()
