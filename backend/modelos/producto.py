# Producto - clase base supertipo para todos los componentes del catalogo
class Producto:
    # __init__ - inicializa los atributos comunes que todo hardware debe tener
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca):
        self.idProducto = idProducto
        self.modeloProducto = modeloProducto
        self.imgUrl = imgUrl
        self.urlOficial = urlOficial
        self.idCategoria = idCategoria
        self.idMarca = idMarca

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idProducto": self.idProducto,
            "modeloProducto": self.modeloProducto,
            "imgUrl": self.imgUrl,
            "urlOficial": self.urlOficial,
            "idCategoria": self.idCategoria,
            "idMarca": self.idMarca
        }