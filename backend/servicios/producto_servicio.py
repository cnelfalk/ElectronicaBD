from dao.producto_dao import ProductoDAO

# ProductoServicio - clase que procesa las reglas de negocio vinculadas al hardware
class ProductoServicio:
    # __init__ - inicializa instanciando el DAO necesario para extraer los datos
    def __init__(self):
        self.productoDao = ProductoDAO()

    # listarProductos - metodo que orquesta la busqueda y prepara la respuesta
    def listarProductos(self, categoria, perfil, busqueda):
        # En el futuro, aqui podriamos agregar logica para calcular puntuaciones
        # o formatear URLs de imagenes rotas antes de enviarlas al frontend
        
        # llamarAlDao - extrae la lista cruda desde la base de datos
        productos = self.productoDao.obtenerCatalogoFiltrado(categoria, perfil, busqueda)
        
        # verificarResultados - estructura el JSON final
        if productos:
            return {"success": True, "data": productos, "total": len(productos)}
        else:
            return {"success": True, "data": [], "mensaje": "No se encontraron productos"}