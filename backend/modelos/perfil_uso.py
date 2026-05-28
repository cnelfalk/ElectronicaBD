# PerfilUso - representa un tipo de perfil de uso para recomendaciones (ej: gaming, ofimatica)
class PerfilUso:
    # __init__ - constructor para inicializar el perfil de uso
    def __init__(self, idPerfil, nombrePerfil):
        self.idPerfil = idPerfil
        self.nombrePerfil = nombrePerfil # Valores esperados: 'gaming', 'ofimatica', 'diseño', 'Desarrollo de Software'

    # to_dict - convierte la instancia en un diccionario
    def to_dict(self):
        return {
            "idPerfil": self.idPerfil,
            "nombrePerfil": self.nombrePerfil
        }
