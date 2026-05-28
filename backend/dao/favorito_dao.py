from database.conexion import ConexionDB

class FavoritoDAO:
    def __init__(self):
        self.conexion = ConexionDB.obtenerInstancia()

    def agregarFavorito(self, idUsuario, idProducto):
        # Usamos INSERT IGNORE para evitar errores si el usuario clickea dos veces
        query = """
            INSERT IGNORE INTO guarda_favorito (id_usuario, id_producto, fecha_agregado_fav) 
            VALUES (%s, %s, NOW())
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idUsuario, idProducto))
            self.conexion.commit()
            return cursor.rowcount > 0 # Retorna True si se insertó, False si ya existía
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAgregarFavorito: {e}")
            return False
        finally:
            cursor.close()

    def obtenerFavoritosPorUsuario(self, idUsuario):
        query = """
            SELECT
                p.id_producto,
                p.modelo_producto as modelo,
                p.img_url,
                c.nombre_categoria as categoria,
                m.nombre_marca as marca,
                gf.fecha_agregado_fav
            FROM guarda_favorito gf
            JOIN productos p ON gf.id_producto = p.id_producto
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN marcas m ON p.id_marca = m.id_marca
            WHERE gf.id_usuario = %s
            ORDER BY gf.fecha_agregado_fav DESC
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idUsuario,))
            return cursor.fetchall()
        except Exception as e:
            print(f"// errorObtenerFavoritos: {e}")
            return []
        finally:
            cursor.close()

    def eliminarFavorito(self, idUsuario, idProducto):
        query = "DELETE FROM guarda_favorito WHERE id_usuario = %s AND id_producto = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idUsuario, idProducto))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorEliminarFavorito: {e}")
            return False
        finally:
            cursor.close()