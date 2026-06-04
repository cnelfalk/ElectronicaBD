import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

def validar_url_retail(url, tienda):
    if not url:
        return False
    url_lower = url.lower()
    if tienda == "Compra Gamer":
        if "compragamer.com/producto/" not in url_lower:
            return False
        # Deben terminar con un ID numérico precedido por guion bajo, ej: _15473
        if not re.search(r'_\d+(?:\?.*)?$', url_lower):
            return False
        return True
    elif tienda == "Mercado Libre":
        if "click1.mercadolibre" in url_lower or "click.mercadolibre" in url_lower or "/mclics/" in url_lower:
            return False
        if "articulo.mercadolibre.com.ar" in url_lower or "/p/mla" in url_lower:
            return True
        return False
    return True

def main():
    conn = ConexionDB.obtenerInstancia()
    if not conn:
        print("Error: No se pudo conectar a la base de datos.")
        return

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.id_producto, s.id_tienda, p.modelo_producto, t.nombre_tienda, s.url_producto 
            FROM se_vende_en s
            JOIN productos p ON s.id_producto = p.id_producto
            JOIN tiendas t ON s.id_tienda = t.id_tienda
        """)
        rows = cursor.fetchall()
        print(f"Total de registros a verificar: {len(rows)}")

        eliminados = 0
        for row in rows:
            tienda = row['nombre_tienda']
            url = row['url_producto']
            id_prod = row['id_producto']
            id_tienda = row['id_tienda']
            modelo = row['modelo_producto']

            if not validar_url_retail(url, tienda):
                print(f"Eliminando enlace invalido: [{tienda}] {modelo[:40]} | URL: {url}")
                cursor.execute("""
                    DELETE FROM se_vende_en 
                    WHERE id_producto = %s AND id_tienda = %s
                """, (id_prod, id_tienda))
                eliminados += 1

        if eliminados > 0:
            conn.commit()
            print(f"Limpieza completada: Se eliminaron {eliminados} registros con enlaces invalidos.")
        else:
            print("No se encontraron enlaces invalidos para eliminar.")

    except Exception as e:
        conn.rollback()
        print(f"Error durante la limpieza de enlaces: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    main()
