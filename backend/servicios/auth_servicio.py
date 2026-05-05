import bcrypt
from dao.usuario_dao import UsuarioDAO
from modelos.usuario import Usuario

# AuthServicio - gestiona la logica de negocio para el registro y login
class AuthServicio:
    # __init__ - inicializa el servicio instanciando su respectivo DAO
    def __init__(self):
        self.usuarioDao = UsuarioDAO()

    # registrarUsuario - valida y cifra los datos antes de guardarlos en BD
    def registrarUsuario(self, nombreUsuario, emailUsuario, contraseniaPlana):
        # verificarDuplicado - comprueba si el correo ya esta registrado
        usuarioExistente = self.usuarioDao.obtenerPorEmail(emailUsuario)
        if usuarioExistente:
            return {"success": False, "mensaje": "El correo ya está registrado"}

        # generarHash - cifra la contraseña utilizando un salt de bcrypt
        salt = bcrypt.gensalt()
        contraseniaHasheada = bcrypt.hashpw(contraseniaPlana.encode('utf-8'), salt)
        
        # crearObjeto - instancia un nuevo usuario con la contraseña protegida (decodificada a string para MySQL)
        nuevoUsuario = Usuario(None, nombreUsuario, emailUsuario, contraseniaHasheada.decode('utf-8'))
        
        # persistirDatos - delega la insercion al DAO
        idGenerado = self.usuarioDao.crearUsuario(nuevoUsuario)
        
        if idGenerado:
            return {"success": True, "mensaje": "Usuario registrado exitosamente"}
        return {"success": False, "mensaje": "Error al registrar en la base de datos"}

    # autenticarUsuario - verifica las credenciales para el inicio de sesion
    def autenticarUsuario(self, emailUsuario, contraseniaPlana):
        # buscarUsuario - recupera el registro completo desde la base de datos
        usuario = self.usuarioDao.obtenerPorEmail(emailUsuario)
        
        if not usuario:
            return {"success": False, "mensaje": "Credenciales inválidas"}

        # compararHash - verifica si la contraseña plana coincide con el hash guardado
        coincide = bcrypt.checkpw(contraseniaPlana.encode('utf-8'), usuario.contraseniaUsuario.encode('utf-8'))
        
        if coincide:
            # omitimos la contrasena en la respuesta por seguridad
            datosUsuario = {
                "idUsuario": usuario.idUsuario,
                "nombreUsuario": usuario.nombreUsuario,
                "emailUsuario": usuario.emailUsuario
            }
            return {"success": True, "datos": datosUsuario}
        
        return {"success": False, "mensaje": "Credenciales inválidas"}