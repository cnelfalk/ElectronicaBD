from modelos.producto import Producto

# Laptop - objeto compuesto que encapsula otros componentes de hardware en su interior
class Laptop(Producto):
    # __init__ - inicializa la laptop recibiendo instancias completas de los componentes internos
    def __init__(self, idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca, cpuObj, gpuObj, ramObj, almacenamientoObj, pesoKg, tamanioPantalla, tasaRefrescoHz, capacidadBateriaWh):
        # llamarConstructorPadre - delega los datos generales a la superclase
        super().__init__(idProducto, modeloProducto, imgUrl, urlOficial, idCategoria, idMarca)
        self.cpu = cpuObj  
        self.gpu = gpuObj  
        self.ram = ramObj  
        self.almacenamiento = almacenamientoObj 
        self.pesoKg = pesoKg
        self.tamanioPantalla = tamanioPantalla
        self.tasaRefrescoHz = tasaRefrescoHz
        self.capacidadBateriaWh = capacidadBateriaWh