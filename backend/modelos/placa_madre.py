from modelos.producto import Producto

# PlacaMadre - clase especializada para placas madre que hereda del supertipo Producto
class PlacaMadre(Producto):
    # __init__ - constructor que extiende los atributos de Producto agregando especificaciones de placa madre
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, idPlacaMadre, formatoPlaca, tipoRamSoportada, idSocket):
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.idPlacaMadre = idPlacaMadre
        self.formatoPlaca = formatoPlaca
        self.tipoRamSoportada = tipoRamSoportada
        self.idSocket = idSocket

    # to_dict - convierte la instancia en un diccionario combinando los campos base y especificos
    def to_dict(self):
        dict_base = super().to_dict()
        dict_base.update({
            "idPlacaMadre": self.idPlacaMadre,
            "formatoPlaca": self.formatoPlaca,
            "tipoRamSoportada": self.tipoRamSoportada,
            "idSocket": self.idSocket
        })
        return dict_base
