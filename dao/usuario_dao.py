"""
usuario_dao.py
--------------
Data Access Object para la entidad Usuario.
Encapsula el SQL: el resto de la app nunca escribe queries directo.
"""

from database.conexion import ConexionDB
from modelos.usuario import Usuario


class UsuarioDAO:
    def __init__(self):
        self._conexion_db = ConexionDB()

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------
    def insertar(self, usuario: Usuario) -> int:
        """Inserta un usuario y devuelve el id autogenerado."""
        sql = """
            INSERT INTO usuarios (nombre, email, contrasenia_hash)
            VALUES (%s, %s, %s)
        """
        conn = self._conexion_db.obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                usuario.nombre,
                usuario.email,
                usuario.contrasenia_hash,
            ))
            conn.commit()
            nuevo_id = cursor.lastrowid
            usuario.id_usuario = nuevo_id
            return nuevo_id
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # SELECT por email (lo usamos en login y para evitar duplicados)
    # ------------------------------------------------------------------
    def buscar_por_email(self, email: str) -> Usuario | None:
        sql = """
            SELECT id_usuario, nombre, email, contrasenia_hash, fec_registro
            FROM usuarios
            WHERE email = %s
        """
        conn = self._conexion_db.obtener_conexion()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (email,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Usuario(
                id_usuario=fila["id_usuario"],
                nombre=fila["nombre"],
                email=fila["email"],
                contrasenia_hash=fila["contrasenia_hash"],
                fec_registro=fila["fec_registro"],
            )
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # SELECT por id (útil para recuperar el usuario logueado por sesión)
    # ------------------------------------------------------------------
    def buscar_por_id(self, id_usuario: int) -> Usuario | None:
        sql = """
            SELECT id_usuario, nombre, email, contrasenia_hash, fec_registro
            FROM usuarios
            WHERE id_usuario = %s
        """
        conn = self._conexion_db.obtener_conexion()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
            if fila is None:
                return None
            return Usuario(
                id_usuario=fila["id_usuario"],
                nombre=fila["nombre"],
                email=fila["email"],
                contrasenia_hash=fila["contrasenia_hash"],
                fec_registro=fila["fec_registro"],
            )
        finally:
            conn.close()