from modelos.producto import Producto

# RAM - clase especializada para memorias de acceso aleatorio que hereda del supertipo Producto
class RAM(Producto):
    # __init__ - constructor que extiende los atributos de Producto agregando especificaciones de RAM
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, idRAM, capacidadGbRam, velocidadMhz, latenciaCl, tipoRam):
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.idRAM = idRAM
        self.capacidadGbRam = capacidadGbRam
        self.velocidadMhz = velocidadMhz
        self.latenciaCl = latenciaCl
        self.tipoRam = tipoRam # 'DDR3', 'DDR4', 'DDR5'

    # to_dict - convierte la instancia en un diccionario combinando los campos base y especificos
    def to_dict(self):
        dict_base = super().to_dict()
        dict_base.update({
            "idRAM": self.idRAM,
            "capacidadGbRam": self.capacidadGbRam,
            "velocidadMhz": self.velocidadMhz,
            "latenciaCl": self.latenciaCl,
            "tipoRam": self.tipoRam
        })
        return dict_base
