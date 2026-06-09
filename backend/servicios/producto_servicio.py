from dao.producto_dao import ProductoDAO
from dao.marca_dao import MarcaDAO
from dao.categoria_dao import CategoriaDAO
from dao.tienda_dao import TiendaDAO

# ProductoServicio - clase que procesa las reglas de negocio vinculadas al hardware
class ProductoServicio:
    # __init__ - inicializa instanciando los DAOs necesarios para extraer los datos
    def __init__(self):
        self.productoDao = ProductoDAO()
        self.marcaDao = MarcaDAO()
        self.categoriaDao = CategoriaDAO()
        self.tiendaDao = TiendaDAO()

    # listarProductos - metodo que orquesta la busqueda y prepara la respuesta
    def listarProductos(self, categoria, perfil, busqueda, marca=None, ordenar=None):
        productos = self.productoDao.obtenerCatalogoFiltrado(categoria, perfil, busqueda, marca, ordenar)

        if productos:
            productos_dict = [p.to_dict() if hasattr(p, 'to_dict') else p for p in productos]
            return {"success": True, "data": productos_dict, "total": len(productos)}
        else:
            return {"success": True, "data": [], "mensaje": "No se encontraron productos"}

    # obtenerMarcas - devuelve solo las marcas que tienen productos en el catálogo
    def obtenerMarcas(self):
        marcas = self.marcaDao.obtenerMarcasConProductos()
        return {"success": True, "data": [m.to_dict() for m in marcas]}

    # obtenerCategorias - devuelve la lista de categorías del sistema
    def obtenerCategorias(self):
        categorias = self.categoriaDao.obtenerCategorias()
        return {"success": True, "data": [c.to_dict() for c in categorias]}

    # obtenerTiendas - devuelve la lista de tiendas registradas
    def obtenerTiendas(self):
        tiendas = self.tiendaDao.obtenerTiendas()
        return {"success": True, "data": [t.to_dict() for t in tiendas]}

    # obtenerDetalle - devuelve el detalle completo de un producto (specs + precios)
    def obtenerDetalle(self, idProducto):
        detalle = self.productoDao.obtenerDetalleProducto(idProducto)
        if not detalle:
            return None
        prod_obj = detalle.get('producto')
        specs_obj = detalle.get('specs')
        return {
            'producto': prod_obj.to_dict() if hasattr(prod_obj, 'to_dict') else prod_obj,
            'specs': specs_obj.to_dict() if hasattr(specs_obj, 'to_dict') else specs_obj,
            'precios': detalle.get('precios')
        }
