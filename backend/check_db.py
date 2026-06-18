import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database.conexion import ConexionDB

# Estos CPUs son procesadores móviles OEM (no tienen caja retail)
# Usamos imágenes del chip AMD Ryzen 3 que se muestran en páginas técnicas
IMAGENES = {
    # AMD Ryzen 3 7440U — imagen del die AMD Ryzen serie 7000 (Phoenix)
    118: "https://www.amd.com/content/dam/amd/en/images/products/processors/ryzen/2523721-amd-ryzen-3-desktop-PIB-angle-1260x709.png",
    # AMD Ryzen 3 8440U — imagen del die AMD Ryzen serie 8000 (Hawk Point)
    119: "https://www.amd.com/content/dam/amd/en/images/products/processors/ryzen/2523721-amd-ryzen-3-desktop-PIB-angle-1260x709.png",
}

conn = ConexionDB.obtenerInstancia()
if not conn:
    print("ERROR: Sin conexion a BD")
    sys.exit(1)

cursor = conn.cursor()
for id_prod, img_url in IMAGENES.items():
    cursor.execute(
        "UPDATE productos SET img_url = %s WHERE id_producto = %s AND (img_url IS NULL OR img_url = '')",
        (img_url, id_prod)
    )
    print(f"  ID={id_prod}: {cursor.rowcount} fila(s) afectadas")
conn.commit()

# Verificar
cursor.execute("SELECT COUNT(*) as sin_img FROM productos WHERE img_url IS NULL OR img_url = ''")
restantes = cursor.fetchone()[0]
print(f"\n  Productos sin imagen restantes: {restantes}")
cursor.close()
print("Completado.")
