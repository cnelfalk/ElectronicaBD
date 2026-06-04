from modelos.producto import Producto

# GPU - clase especializada para tarjetas de video que hereda del supertipo Producto
class GPU(Producto):
    # __init__ - constructor que extiende los atributos de Producto agregando especificaciones de GPU
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, idGPU, vram, tipoMemoria, consumoWh):
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.idGPU = idGPU
        self.vram = vram
        self.tipoMemoria = tipoMemoria
        self.consumoWh = consumoWh

    # to_dict - convierte la instancia en un diccionario combinando los campos base y especificos
    def to_dict(self):
        dict_base = super().to_dict()
        dict_base.update({
            "idGPU": self.idGPU,
            "vram": self.vram,
            "tipoMemoria": self.tipoMemoria,
            "consumoWh": self.consumoWh,
            
            # Compatibilidad con frontend (snake_case)
            "vram_gb": self.vram,
            "tipo_memoria": self.tipoMemoria,
            "tdp_w": self.consumoWh,
            "consumo_wh": self.consumoWh
        })
        return dict_base
