"""
auth_servicio.py
----------------
Lógica de negocio de autenticación.
Usa `bcrypt` para hashear contraseñas (nunca las guardamos en texto plano).

La clase se ubica entre las rutas Flask y el DAO:
    [ruta Flask] -> AuthServicio.registrar() -> UsuarioDAO.insertar()
"""

import bcrypt
from dao.usuario_dao import UsuarioDAO
from modelos.usuario import Usuario


class EmailYaRegistradoError(Exception):
    """Se lanza cuando alguien intenta registrarse con un email existente."""


class CredencialesInvalidasError(Exception):
    """Se lanza cuando email o contraseña no coinciden en el login."""


class AuthServicio:
    def __init__(self):
        self._usuario_dao = UsuarioDAO()

    # ------------------------------------------------------------------
    # REGISTRO
    # ------------------------------------------------------------------
    def registrar(self, nombre: str, email: str, contrasenia: str) -> Usuario:
        """Crea un usuario nuevo. Lanza EmailYaRegistradoError si ya existe."""
        if self._usuario_dao.buscar_por_email(email) is not None:
            raise EmailYaRegistradoError(f"El email '{email}' ya está registrado.")

        hash_pw = self._hashear(contrasenia)
        nuevo = Usuario(
            nombre=nombre.strip(),
            email=email.strip().lower(),
            contrasenia_hash=hash_pw,
        )
        self._usuario_dao.insertar(nuevo)
        return nuevo

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------
    def iniciar_sesion(self, email: str, contrasenia: str) -> Usuario:
        """Valida credenciales. Devuelve el usuario si todo ok."""
        usuario = self._usuario_dao.buscar_por_email(email.strip().lower())
        if usuario is None:
            raise CredencialesInvalidasError("Email o contraseña incorrectos.")

        if not self._verificar(contrasenia, usuario.contrasenia_hash):
            raise CredencialesInvalidasError("Email o contraseña incorrectos.")

        return usuario

    # ------------------------------------------------------------------
    # Helpers privados de hashing
    # ------------------------------------------------------------------
    @staticmethod
    def _hashear(contrasenia: str) -> str:
        hash_bytes = bcrypt.hashpw(contrasenia.encode("utf-8"), bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    @staticmethod
    def _verificar(contrasenia: str, hash_guardado: str) -> bool:
        return bcrypt.checkpw(
            contrasenia.encode("utf-8"),
            hash_guardado.encode("utf-8"),
        )