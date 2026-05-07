<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand fw-bold" href="catalogo.php">TechMatch</a>

        <div class="d-flex align-items-center gap-2">
            <!-- Estado: no logueado -->
            <div id="nav-sin-sesion">
                <a href="login.php" class="btn btn-outline-light btn-sm me-1">Iniciar Sesión</a>
                <a href="registro.php" class="btn btn-primary btn-sm">Registrarse</a>
            </div>

            <!-- Estado: logueado (oculto hasta que JS lo muestre) -->
            <div id="nav-con-sesion" style="display:none;" class="d-flex align-items-center gap-2">
                <span class="text-light small" id="nav-nombre-usuario"></span>
                <button class="btn btn-outline-light btn-sm" onclick="cerrarSesion()">Cerrar Sesión</button>
            </div>
        </div>
    </div>
</nav>

<script>
    (function () {
        const datos = localStorage.getItem('techmatch_usuario');
        if (datos) {
            const usuario = JSON.parse(datos);
            document.getElementById('nav-sin-sesion').style.display = 'none';
            document.getElementById('nav-con-sesion').style.display = 'flex';
            document.getElementById('nav-nombre-usuario').textContent = 'Hola, ' + usuario.nombreUsuario;
        }
    })();

    function cerrarSesion() {
        localStorage.removeItem('techmatch_usuario');
        window.location.href = 'catalogo.php';
    }
</script>
