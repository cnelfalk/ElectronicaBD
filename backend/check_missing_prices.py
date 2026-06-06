import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

def main():
    conn = ConexionDB.obtenerInstancia()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT p.id_producto, p.modelo_producto as modelo, m.nombre_marca as marca, c.nombre_categoria as categoria
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        JOIN marcas m ON p.id_marca = m.id_marca
        LEFT JOIN producto_tienda s ON p.id_producto = s.id_producto
        WHERE s.id_producto IS NULL
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    print(f"Total de productos sin precio ni link: {len(resultados)}")
    for r in resultados[:20]:
        print(f"- [{r['categoria']}] {r['marca']} : {r['modelo']}")

    cursor.close()

if __name__ == "__main__":
    main()
