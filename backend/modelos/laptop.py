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

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        d = super().to_dict()
        d.update({
            "cpu": self.cpu.to_dict() if hasattr(self.cpu, "to_dict") else self.cpu,
            "gpu": self.gpu.to_dict() if hasattr(self.gpu, "to_dict") else self.gpu,
            "ram": self.ram.to_dict() if hasattr(self.ram, "to_dict") else self.ram,
            "almacenamiento": self.almacenamiento.to_dict() if hasattr(self.almacenamiento, "to_dict") else self.almacenamiento,
            "pesoKg": self.pesoKg,
            "tamanioPantalla": self.tamanioPantalla,
            "tasaRefrescoHz": self.tasaRefrescoHz,
            "capacidadBateriaWh": self.capacidadBateriaWh,
            
            # Compatibilidad con frontend (snake_case)
            "cpu_modelo": self.cpu,
            "gpu_modelo": self.gpu,
            "ram_gb": self.ram,
            "almacenamiento_gb": self.almacenamiento,
            "peso_kg": self.pesoKg,
            "tamanio_pantalla": self.tamanioPantalla,
            "tasa_refresco_hz": self.tasaRefrescoHz,
            "capacidad_bateria_wh": self.capacidadBateriaWh
        })
        return d