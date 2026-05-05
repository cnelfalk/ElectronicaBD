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