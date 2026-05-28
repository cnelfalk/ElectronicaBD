# Marca - representa la marca fabricante de un producto
class Marca:
    # __init__ - constructor para inicializar la marca con sus atributos
    def __init__(self, idMarca, nombreMarca, urlMarca=None):
        self.idMarca = idMarca
        self.nombreMarca = nombreMarca
        self.urlMarca = urlMarca

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idMarca": self.idMarca,
            "nombreMarca": self.nombreMarca,
            "urlMarca": self.urlMarca
        }
