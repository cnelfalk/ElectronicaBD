from database.conexion import ConexionDB
from modelos.usuario import Usuario

# UsuarioDAO - gestiona las operaciones de base de datos para la entidad usuarios
class UsuarioDAO:
    @property
    def conexion(self):
        return ConexionDB.obtenerInstancia()

    # obtenerPorIdentificador - busca un usuario utilizando su correo electronico o nombre de usuario
    def obtenerPorIdentificador(self, identificador):
        # prepararConsulta - define el query SQL previniendo inyecciones SQL
        # ACÁ ESTÁ EL CAMBIO: Buscamos por email O por nombre
        query = "SELECT * FROM usuarios WHERE email_usuario = %s OR nombre_usuario = %s"
        cursor = self.conexion.cursor(dictionary=True)
        try:
            # Pasamos el identificador dos veces para que reemplace ambos %s
            cursor.execute(query, (identificador, identificador))
            registro = cursor.fetchone()
        except Exception as e:
            print(f"// errorObtenerPorIdentificador: {e}")
            return None
        finally:
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
        query = "INSERT INTO usuarios (nombre_usuario, email_usuario, contrasenia_usuario) VALUES (%s, %s, %s)"
        cursor = self.conexion.cursor()

        try:
            valores = (usuario.nombreUsuario, usuario.emailUsuario, usuario.contraseniaUsuario)
            cursor.execute(query, valores)
            self.conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlCrearUsuario: {e}")
            return None
        finally:
            cursor.close()

    # actualizarContrasenia - actualiza la contraseña hasheada de un usuario existente
    def actualizarContrasenia(self, idUsuario, nuevaContraseniaHash):
        query = "UPDATE usuarios SET contrasenia_usuario = %s WHERE id_usuario = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (nuevaContraseniaHash, idUsuario))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlActualizarContrasenia: {e}")
            return False
        finally:
            cursor.close()