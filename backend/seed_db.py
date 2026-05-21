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
    # Seed marcas
    marcas = [
        (1, 'Asus', 'https://www.asus.com'),
        (2, 'Lenovo', 'https://www.lenovo.com'),
        (3, 'AMD', 'https://www.amd.com'),
        (4, 'Intel', 'https://www.intel.com'),
        (5, 'NVIDIA', 'https://www.nvidia.com')
    ]
    for id_marca, nombre, url in marcas:
        cursor.execute("""
            INSERT INTO marcas (id_marca, nombre_marca, url_marca) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE nombre_marca = VALUES(nombre_marca), url_marca = VALUES(url_marca)
        """, (id_marca, nombre, url))
    print("Seed marcas: OK")

    # Seed categorias
    categorias = [
        (1, 'Laptop'),
        (2, 'CPU'),
        (3, 'GPU'),
        (4, 'RAM'),
        (5, 'Almacenamiento')
    ]
    for id_cat, nombre in categorias:
        cursor.execute("""
            INSERT INTO categorias (id_categoria, nombre_categoria)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE nombre_categoria = VALUES(nombre_categoria)
        """, (id_cat, nombre))
    print("Seed categorias: OK")

    # Seed tiendas
    tiendas = [
        (1, 'Mercado Libre', 'https://www.mercadolibre.com.ar'),
        (2, 'Compra Gamer', 'https://www.compragamer.com')
    ]
    for id_tienda, nombre, url in tiendas:
        cursor.execute("""
            INSERT INTO tiendas (id_tienda, nombre_tienda, url_tienda)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE nombre_tienda = VALUES(nombre_tienda), url_tienda = VALUES(url_tienda)
        """, (id_tienda, nombre, url))
    print("Seed tiendas: OK")

    # Seed sockets
    sockets = [
        (1, 'BGA / Soldered'),
        (2, 'AM4'),
        (3, 'AM5'),
        (4, 'LGA1700'),
        (5, 'LGA1851'),
        (6, 'N/A')
    ]
    for id_sock, nombre in sockets:
        cursor.execute("""
            INSERT INTO socket (id_socket, nombre_socket)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE nombre_socket = VALUES(nombre_socket)
        """, (id_sock, nombre))
    print("Seed sockets: OK")

    # Seed perfiles_uso
    perfiles = [
        (1, 'gaming'),
        (2, 'ofimatica'),
        (3, 'diseño'),
        (4, 'Desarrollo de Software')
    ]
    for id_perf, nombre in perfiles:
        cursor.execute("""
            INSERT INTO perfiles_uso (id_perfil, nombre_perfil)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE nombre_perfil = VALUES(nombre_perfil)
        """, (id_perf, nombre))
    print("Seed perfiles_uso: OK")

    conn.commit()
    print("All seeds committed successfully!")
except Exception as e:
    conn.rollback()
    print(f"Error seeding DB: {e}")
finally:
    cursor.close()
