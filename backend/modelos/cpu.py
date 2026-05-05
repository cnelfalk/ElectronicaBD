from modelos.producto import Producto

# CPU - clase especializada para procesadores que hereda del supertipo Producto
class CPU(Producto):
    # __init__ - constructor que extiende los atributos base agregando especificaciones tecnicas
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, nucleos, hilos, frecuenciaBase, frecuenciaTurbo, tdp, idSocket):
        # llamarConstructorPadre - inicializa los atributos heredados de la clase Producto
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.nucleos = nucleos
        self.hilos = hilos
        self.frecuenciaBase = frecuenciaBase
        self.frecuenciaTurbo = frecuenciaTurbo
        self.tdp = tdp
        self.idSocket = idSocket