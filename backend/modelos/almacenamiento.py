from modelos.producto import Producto

# Almacenamiento - clase especializada para unidades de almacenamiento (SSD, HDD) que hereda del supertipo Producto
class Almacenamiento(Producto):
    # __init__ - constructor que extiende los atributos de Producto agregando especificaciones de almacenamiento
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, idAlmacenamiento, capacidadGbAlmacenamiento, tipoAlmacenamiento, velLectura=None, velEscritura=None):
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.idAlmacenamiento = idAlmacenamiento
        self.capacidadGbAlmacenamiento = capacidadGbAlmacenamiento
        self.tipoAlmacenamiento = tipoAlmacenamiento
        self.velLectura = velLectura
        self.velEscritura = velEscritura

    # to_dict - convierte la instancia en un diccionario combinando los campos base y especificos
    def to_dict(self):
        dict_base = super().to_dict()
        dict_base.update({
            "idAlmacenamiento": self.idAlmacenamiento,
            "capacidadGbAlmacenamiento": self.capacidadGbAlmacenamiento,
            "tipoAlmacenamiento": self.tipoAlmacenamiento,
            "velLectura": self.velLectura,
            "velEscritura": self.velEscritura,
            
            # Compatibilidad con frontend 
            "capacidad_gb": self.capacidadGbAlmacenamiento,
            "tipo_disco": self.tipoAlmacenamiento,
            "tipo_almacenamiento": self.tipoAlmacenamiento,
            "velocidad_lectura": self.velLectura,
            "vel_lectura": self.velLectura,
            "vel_escritura": self.velEscritura
        })
        return dict_base
