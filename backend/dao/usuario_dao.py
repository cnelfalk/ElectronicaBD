from database.conexion import ConexionDB
from modelos.usuario import Usuario

# UsuarioDAO - gestiona las operaciones de base de datos para la entidad Usuarios
class UsuarioDAO:
    # __init__ - inicializa el DAO obteniendo la conexion unica a la base de datos
    def __init__(self):
        self.conexion = ConexionDB.obtenerInstancia()

    # obtenerPorEmail - busca un usuario especifico utilizando su correo electronico
    def obtenerPorEmail(self, emailUsuario):
        # prepararConsulta - define el query SQL previniendo inyecciones SQL
        query = "SELECT * FROM Usuarios WHERE email_usuario = %s"
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(query, (emailUsuario,))
        registro = cursor.fetchone()
        cursor.close()

        if registro:
            # mapearObjeto - convierte el diccionario de BD en un objeto Usuario
            return Usuario(
                idUsuario=registro['id_usuario'],
                nombreUsuario=registro['nombre_usuario'],
                emailUsuario=registro['email_usuario'],
                contraseniaUsuario=registro['contrasenia_usuario'],
                fecRegistro=registro['fec_registro']
            )
        return None

    # crearUsuario - inserta un nuevo registro de usuario en la base de datos
    def crearUsuario(self, usuario):
        # insertarRegistro - ejecuta el insert devolviendo el ID generado
        query = "INSERT INTO Usuarios (nombre_usuario, email_usuario, contrasenia_usuario) VALUES (%s, %s, %s)"
        cursor = self.conexion.cursor()
        
        try:
            valores = (usuario.nombreUsuario, usuario.emailUsuario, usuario.contraseniaUsuario)
            cursor.execute(query, valores)
            self.conexion.commit()
            nuevoId = cursor.lastrowid
            cursor.close()
            return nuevoId
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlCrearUsuario: {e}")
            return None