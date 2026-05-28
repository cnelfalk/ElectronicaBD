# Tienda - representa un comercio o plataforma donde se venden productos
class Tienda:
    # __init__ - constructor para inicializar la tienda
    def __init__(self, idTienda, nombreTienda, urlTienda=None):
        self.idTienda = idTienda
        self.nombreTienda = nombreTienda
        self.urlTienda = urlTienda

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idTienda": self.idTienda,
            "nombreTienda": self.nombreTienda,
            "urlTienda": self.urlTienda
        }
