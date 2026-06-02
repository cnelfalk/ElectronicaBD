from dao.producto_dao import ProductoDAO

# ProductoServicio - clase que procesa las reglas de negocio vinculadas al hardware
class ProductoServicio:
    # __init__ - inicializa instanciando el DAO necesario para extraer los datos
    def __init__(self):
        self.productoDao = ProductoDAO()

    # listarProductos - metodo que orquesta la busqueda y prepara la respuesta
    def listarProductos(self, categoria, perfil, busqueda, marca=None, ordenar=None):
        productos = self.productoDao.obtenerCatalogoFiltrado(categoria, perfil, busqueda, marca, ordenar)

        if productos:
            return {"success": True, "data": productos, "total": len(productos)}
        else:
            return {"success": True, "data": [], "mensaje": "No se encontraron productos"}

    # obtenerMarcas - devuelve la lista de marcas con productos para poblar el filtro del catálogo
    def obtenerMarcas(self):
        marcas = self.productoDao.obtenerMarcasConProductos()
        return {"success": True, "data": marcas}

    # obtenerDetalle - devuelve el detalle completo de un producto (specs + precios)
    def obtenerDetalle(self, idProducto):
        return self.productoDao.obtenerDetalleProducto(idProducto)
