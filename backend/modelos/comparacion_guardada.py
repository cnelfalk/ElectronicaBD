# ComparacionGuardada - representa una comparacion de productos guardada por un usuario
class ComparacionGuardada:
    # __init__ - constructor de la clase para inicializar una comparacion guardada
    def __init__(self, idComparacion, fecCreacionComp, idCategoria, idUsuario, productos=None):
        self.idComparacion = idComparacion
        self.fecCreacionComp = fecCreacionComp
        self.idCategoria = idCategoria
        self.idUsuario = idUsuario
        self.productos = productos if productos is not None else [] # Lista de productos o IDs de productos comparados

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        # Si los elementos en productos tienen to_dict, los convertimos, sino los dejamos como estan (p.ej. si son IDs)
        serializados_productos = []
        for p in self.productos:
            if hasattr(p, 'to_dict'):
                serializados_productos.append(p.to_dict())
            else:
                serializados_productos.append(p)

        return {
            "idComparacion": self.idComparacion,
            "fecCreacionComp": self.fecCreacionComp.isoformat() if hasattr(self.fecCreacionComp, 'isoformat') else self.fecCreacionComp,
            "idCategoria": self.idCategoria,
            "idUsuario": self.idUsuario,
            "productos": serializados_productos
        }
