from modelos.producto import Producto

# CPU - clase especializada para procesadores que hereda del supertipo Producto
class CPU(Producto):
    # __init__ - constructor que extiende los atributos base agregando especificaciones tecnicas
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, nucleos, hilos, frecuenciaBase, frecuenciaTurbo, tdp):
        # llamarConstructorPadre - inicializa los atributos heredados de la clase Producto
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.nucleos = nucleos
        self.hilos = hilos
        self.frecuenciaBase = frecuenciaBase
        self.frecuenciaTurbo = frecuenciaTurbo
        self.tdp = tdp

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        d = super().to_dict()
        d.update({
            "nucleos": self.nucleos,
            "hilos": self.hilos,
            "frecuenciaBase": self.frecuenciaBase,
            "frecuenciaTurbo": self.frecuenciaTurbo,
            "tdp": self.tdp,

            # Compatibilidad con frontend (snake_case)
            "frecuencia_base": self.frecuenciaBase,
            "frecuencia_turbo": self.frecuenciaTurbo,
        })
        return d