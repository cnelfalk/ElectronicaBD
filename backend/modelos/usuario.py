# Usuario - representa a un usuario registrado en el sistema TechMatch
class Usuario:
    # __init__ - constructor de la clase para inicializar al usuario
    def __init__(self, idUsuario, nombreUsuario, emailUsuario, contraseniaUsuario, fecRegistro=None):
        self.idUsuario = idUsuario
        self.nombreUsuario = nombreUsuario
        self.emailUsuario = emailUsuario
        self.contraseniaUsuario = contraseniaUsuario
        self.fecRegistro = fecRegistro