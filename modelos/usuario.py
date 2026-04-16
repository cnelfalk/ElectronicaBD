"""
usuario.py
----------
Clase de dominio `Usuario`. Representa a un usuario registrado.
No tiene lógica de persistencia (eso vive en UsuarioDAO).
"""

from datetime import datetime


class Usuario:
    def __init__(
        self,
        nombre: str,
        email: str,
        contrasenia_hash: str,
        id_usuario: int | None = None,
        fec_registro: datetime | None = None,
    ):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._email = email
        self._contrasenia_hash = contrasenia_hash
        self._fec_registro = fec_registro

    # ---- properties (encapsulamiento) ----
    @property
    def id_usuario(self) -> int | None:
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor: int) -> None:
        self._id_usuario = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @property
    def contrasenia_hash(self) -> str:
        return self._contrasenia_hash

    @property
    def fec_registro(self) -> datetime | None:
        return self._fec_registro

    def __repr__(self) -> str:
        return f"<Usuario id={self._id_usuario} email={self._email}>"