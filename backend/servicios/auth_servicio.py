import bcrypt
import secrets
from datetime import datetime, timedelta
from dao.usuario_dao import UsuarioDAO
from dao.recuperacion_dao import RecuperacionDAO
from servicios.email_servicio import EmailServicio
from modelos.usuario import Usuario

# AuthServicio - gestiona la logica de negocio para el registro y login
class AuthServicio:
    # __init__ - inicializa el servicio instanciando su respectivo DAO
    def __init__(self):
        self.usuarioDao = UsuarioDAO()
        self.recuperacionDao = RecuperacionDAO()
        self.emailServicio = EmailServicio()

    # registrarUsuario - valida y cifra los datos antes de guardarlos en BD
    def registrarUsuario(self, nombreUsuario, emailUsuario, contraseniaPlana):
        # Validar límites de la base de datos
        if len(nombreUsuario) > 30:
            return {"success": False, "mensaje": "Incorrecto: El nombre de usuario no debe superar los 30 caracteres."}
        if len(emailUsuario) > 150:
            return {"success": False, "mensaje": "Incorrecto: El correo electrónico no debe superar los 150 caracteres."}
        if len(contraseniaPlana) > 255:
            return {"success": False, "mensaje": "Incorrecto: La contraseña no debe superar los 255 caracteres."}

        # Validar si el correo o el nombre de usuario ya existen en la base de datos
        usuarioExistenteEmail = self.usuarioDao.obtenerPorIdentificador(emailUsuario)
        if usuarioExistenteEmail:
            return {"success": False, "mensaje": "El correo ya está registrado"}

        usuarioExistenteNombre = self.usuarioDao.obtenerPorIdentificador(nombreUsuario)
        if usuarioExistenteNombre:
            return {"success": False, "mensaje": "El nombre de usuario ya está registrado"}

        # generarHash - cifra la contraseña utilizando un salt de bcrypt
        salt = bcrypt.gensalt()
        contraseniaHasheada = bcrypt.hashpw(contraseniaPlana.encode('utf-8'), salt)
        
        # crearObjeto - instancia un nuevo usuario con la contraseña protegida
        nuevoUsuario = Usuario(None, nombreUsuario, emailUsuario, contraseniaHasheada.decode('utf-8'))
        
        # persistirDatos - delega la insercion al DAO
        idGenerado = self.usuarioDao.crearUsuario(nuevoUsuario)
        
        if idGenerado:
            return {"success": True, "mensaje": "Usuario registrado exitosamente"}
        return {"success": False, "mensaje": "Error al registrar en la base de datos"}

    # autenticarUsuario - verifica las credenciales para el inicio de sesion
    def autenticarUsuario(self, identificador, contraseniaPlana):
        # CAMBIO: Usamos la nueva función del DAO
        usuario = self.usuarioDao.obtenerPorIdentificador(identificador)
        
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

    # ══════════════════════════════════════════════════════
    #  RECUPERACIÓN DE CONTRASEÑA
    # ══════════════════════════════════════════════════════

    # solicitarRecuperacion - genera un código de 6 dígitos, lo guarda en BD y lo envía por email
    def solicitarRecuperacion(self, emailUsuario):
        # CAMBIO: Aunque solo pidamos el correo, el método en el DAO se llama obtenerPorIdentificador
        usuario = self.usuarioDao.obtenerPorIdentificador(emailUsuario)
        
        if not usuario:
            # mensajeGenerico - por seguridad, no revelamos si el email existe o no
            return {"success": True, "mensaje": "Si el correo está registrado, recibirás un código de recuperación."}

        # generarCodigo - código numérico de 6 dígitos usando secrets para mayor seguridad
        codigo = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        # establecerExpiracion - el código vence en 15 minutos
        fecExpiracion = datetime.now() + timedelta(minutes=15)

        # persistirCodigo - guardamos el código en la tabla codigos_recuperacion
        idCodigo = self.recuperacionDao.crearCodigo(usuario.idUsuario, codigo, fecExpiracion)
        
        if not idCodigo:
            return {"success": False, "mensaje": "Error al generar el código de recuperación."}

        # enviarEmail - despachamos el correo con el código al usuario
        emailEnviado = self.emailServicio.enviarCodigoRecuperacion(
            emailUsuario, usuario.nombreUsuario, codigo
        )

        if not emailEnviado:
            return {"success": False, "mensaje": "No se pudo enviar el correo. Intentá de nuevo en unos minutos."}

        return {"success": True, "mensaje": "Si el correo está registrado, recibirás un código de recuperación."}

    # verificarCodigo - valida el código ingresado por el usuario y genera un token temporal
    def verificarCodigo(self, emailUsuario, codigo):
        # CAMBIO: Usamos la nueva función del DAO
        usuario = self.usuarioDao.obtenerPorIdentificador(emailUsuario)
        
        if not usuario:
            return {"success": False, "mensaje": "Código inválido o expirado."}

        # consultarCodigo - buscamos un código válido, no usado y no expirado
        registro = self.recuperacionDao.verificarCodigo(usuario.idUsuario, codigo)
        
        if not registro:
            return {"success": False, "mensaje": "Código inválido o expirado."}

        # generarToken - creamos un token temporal seguro para el paso de cambio de contraseña
        token = secrets.token_hex(32)
        
        # guardarToken - asociamos el token al código verificado
        self.recuperacionDao.guardarToken(registro['id_codigo'], token)

        return {"success": True, "token": token, "mensaje": "Código verificado correctamente."}

    # cambiarContrasenia - actualiza la contraseña del usuario tras verificar el token
    def cambiarContrasenia(self, emailUsuario, token, nuevaContrasenia):
        # CAMBIO: Usamos la nueva función del DAO
        usuario = self.usuarioDao.obtenerPorIdentificador(emailUsuario)
        
        if not usuario:
            return {"success": False, "mensaje": "Error al procesar la solicitud."}

        # validarToken - verificamos que el token sea correcto y esté vigente
        registro = self.recuperacionDao.verificarToken(usuario.idUsuario, token)
        
        if not registro:
            return {"success": False, "mensaje": "Token inválido o expirado. Solicitá un nuevo código."}

        # hashearNuevaContrasenia - ciframos la nueva contraseña con bcrypt
        salt = bcrypt.gensalt()
        nuevaContraseniaHash = bcrypt.hashpw(nuevaContrasenia.encode('utf-8'), salt).decode('utf-8')

        # actualizarEnBD - persistimos la nueva contraseña
        actualizado = self.usuarioDao.actualizarContrasenia(usuario.idUsuario, nuevaContraseniaHash)
        
        if not actualizado:
            return {"success": False, "mensaje": "Error al actualizar la contraseña."}

        # limpiarCodigos - eliminamos todos los códigos del usuario por seguridad
        self.recuperacionDao.marcarComoUsado(registro['id_codigo'])
        self.recuperacionDao.eliminarCodigosUsuario(usuario.idUsuario)

        return {"success": True, "mensaje": "Contraseña actualizada exitosamente."}