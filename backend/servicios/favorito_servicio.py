from dao.favorito_dao import FavoritoDAO

class FavoritoServicio:
    def __init__(self):
        self.favoritoDao = FavoritoDAO()

    def agregar(self, idUsuario, idProducto):
        if not idUsuario or not idProducto:
            return {"success": False, "mensaje": "Faltan datos requeridos"}
            
        exito = self.favoritoDao.agregarFavorito(idUsuario, idProducto)
        if exito:
            return {"success": True, "mensaje": "Producto guardado en favoritos"}
        return {"success": True, "mensaje": "El producto ya estaba en tus favoritos"}

    def listar(self, idUsuario):
        if not idUsuario:
            return {"success": False, "mensaje": "ID de usuario no proporcionado"}
            
        favoritos = self.favoritoDao.obtenerFavoritosPorUsuario(idUsuario)
        return {"success": True, "data": favoritos, "total": len(favoritos)}

    def eliminar(self, idUsuario, idProducto):
        exito = self.favoritoDao.eliminarFavorito(idUsuario, idProducto)
        if exito:
            return {"success": True, "mensaje": "Favorito eliminado correctamente"}
        return {"success": False, "mensaje": "No se pudo eliminar el favorito"}