from database.conexion import ConexionDB
from datetime import datetime

# RecuperacionDAO - gestiona las operaciones de BD para códigos de recuperación de contraseña
class RecuperacionDAO:
    @property
    def conexion(self):
        return ConexionDB.obtenerInstancia()

    # crearCodigo - inserta un nuevo código de recuperación para un usuario
    def crearCodigo(self, idUsuario, codigo, fecExpiracion):
        # invalidarAnteriores - marca como usados todos los códigos previos del usuario para que no se acumulen
        self._invalidarCodigosAnteriores(idUsuario)

        query = """
            INSERT INTO codigos_recuperacion (id_usuario, codigo, fec_expiracion)
            VALUES (%s, %s, %s)
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idUsuario, codigo, fecExpiracion))
            self.conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlCrearCodigo: {e}")
            return None
        finally:
            cursor.close()

    # verificarCodigo - busca un código válido (no expirado, no usado) para el usuario
    def verificarCodigo(self, idUsuario, codigo):
        query = """
            SELECT id_codigo, codigo, fec_expiracion, usado
            FROM codigos_recuperacion
            WHERE id_usuario = %s AND codigo = %s AND usado = 0 AND fec_expiracion > NOW()
            ORDER BY fec_creacion DESC
            LIMIT 1
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idUsuario, codigo))
            return cursor.fetchone()
        except Exception as e:
            print(f"// errorAlVerificarCodigo: {e}")
            return None
        finally:
            cursor.close()

    # guardarToken - almacena el token de verificación tras validar el código exitosamente
    def guardarToken(self, idCodigo, token):
        query = """
            UPDATE codigos_recuperacion
            SET token_verificacion = %s
            WHERE id_codigo = %s
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (token, idCodigo))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlGuardarToken: {e}")
            return False
        finally:
            cursor.close()

    # verificarToken - valida que el token sea correcto, no usado y no expirado
    def verificarToken(self, idUsuario, token):
        query = """
            SELECT id_codigo
            FROM codigos_recuperacion
            WHERE id_usuario = %s AND token_verificacion = %s AND usado = 0 AND fec_expiracion > NOW()
            LIMIT 1
        """
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute(query, (idUsuario, token))
            return cursor.fetchone()
        except Exception as e:
            print(f"// errorAlVerificarToken: {e}")
            return None
        finally:
            cursor.close()

    # marcarComoUsado - marca el código como utilizado para que no se pueda reutilizar
    def marcarComoUsado(self, idCodigo):
        query = "UPDATE codigos_recuperacion SET usado = 1 WHERE id_codigo = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idCodigo,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlMarcarComoUsado: {e}")
            return False
        finally:
            cursor.close()

    # eliminarCodigosUsuario - limpia todos los códigos de un usuario (usado tras cambio exitoso)
    def eliminarCodigosUsuario(self, idUsuario):
        query = "DELETE FROM codigos_recuperacion WHERE id_usuario = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idUsuario,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlEliminarCodigos: {e}")
            return False
        finally:
            cursor.close()

    # _invalidarCodigosAnteriores - marca como usados los códigos previos del usuario
    def _invalidarCodigosAnteriores(self, idUsuario):
        query = "UPDATE codigos_recuperacion SET usado = 1 WHERE id_usuario = %s AND usado = 0"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(query, (idUsuario,))
            self.conexion.commit()
        except Exception as e:
            self.conexion.rollback()
            print(f"// errorAlInvalidarCodigos: {e}")
        finally:
            cursor.close()
