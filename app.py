"""
app.py
------
Aplicación Flask de TechMatch (MVP).

Rutas:
    GET  /             -> redirige a /login o /productos según sesión
    GET  /registro     -> formulario de registro
    POST /registro     -> procesa el registro
    GET  /login        -> formulario de login
    POST /login        -> procesa el login
    GET  /logout       -> cierra sesión
    GET  /productos    -> vista de productos (requiere login)

Para correr:
    python app.py
Y abrir en el navegador:
    http://127.0.0.1:5000
"""

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session

from config import Config
from servicios.auth_servicio import (
    AuthServicio,
    EmailYaRegistradoError,
    CredencialesInvalidasError,
)


# ---------------------------------------------------------------------
# Inicialización de la app
# ---------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

auth_servicio = AuthServicio()


# ---------------------------------------------------------------------
# Decorador: exige que el usuario esté logueado para acceder a una ruta
# ---------------------------------------------------------------------
def login_requerido(vista):
    @wraps(vista)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------
@app.route("/")
def index():
    if "id_usuario" in session:
        return redirect(url_for("productos"))
    return redirect(url_for("login"))


# ---- REGISTRO ----
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")

    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    contrasenia = request.form.get("contrasenia", "")

    if not nombre or not email or not contrasenia:
        return render_template("registro.html", error="Completá todos los campos.")

    try:
        auth_servicio.registrar(nombre, email, contrasenia)
    except EmailYaRegistradoError as e:
        return render_template("registro.html", error=str(e))
    except Exception as e:
        return render_template("registro.html", error=f"Error inesperado: {e}")

    # Registro exitoso -> lo mandamos al login para que entre
    return redirect(url_for("login"))


# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    contrasenia = request.form.get("contrasenia", "")

    try:
        usuario = auth_servicio.iniciar_sesion(email, contrasenia)
    except CredencialesInvalidasError as e:
        return render_template("login.html", error=str(e))
    except Exception as e:
        return render_template("login.html", error=f"Error inesperado: {e}")

    # Guardamos datos mínimos en la sesión (cookie firmada por Flask)
    session["id_usuario"] = usuario.id_usuario
    session["nombre"] = usuario.nombre
    return redirect(url_for("productos"))


# ---- LOGOUT ----
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---- PRODUCTOS (ejemplo protegido) ----
@app.route("/productos")
@login_requerido
def productos():
    # TODO: reemplazar por consulta real vía ProductoDAO cuando
    # conectemos el bot y empiece a llenar la base.
    return render_template(
        "productos.html",
        usuario=session.get("nombre", ""),
        productos=[],
        ultima_actualizacion=None,
    )


# ---------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)