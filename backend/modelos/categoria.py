# Categoria - representa el tipo de producto en el sistema (ej: Laptop, CPU, etc.)
class Categoria:
    # __init__ - constructor para inicializar la categoria
    def __init__(self, idCategoria, nombreCategoria):
        self.idCategoria = idCategoria
        self.nombreCategoria = nombreCategoria

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idCategoria": self.idCategoria,
            "nombreCategoria": self.nombreCategoria
        }
