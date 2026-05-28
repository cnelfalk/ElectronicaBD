# ProductoPerfil - representa la relacion muchos a muchos entre un producto y un perfil de uso
class ProductoPerfil:
    # __init__ - constructor para inicializar la relacion intermedia
    def __init__(self, idPerfil, idProducto):
        self.idPerfil = idPerfil
        self.idProducto = idProducto

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idPerfil": self.idPerfil,
            "idProducto": self.idProducto
        }
