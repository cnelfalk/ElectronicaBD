# Socket - representa el zocalo de conexion para CPUs y Placas Madre
class Socket:
    # __init__ - constructor para inicializar el socket
    def __init__(self, idSocket, nombreSocket):
        self.idSocket = idSocket
        self.nombreSocket = nombreSocket

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idSocket": self.idSocket,
            "nombreSocket": self.nombreSocket
        }
