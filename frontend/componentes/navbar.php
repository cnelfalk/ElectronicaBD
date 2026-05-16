<nav class="tm-navbar">
    <div class="tm-navbar-inner">
        <a class="tm-logo" href="catalogo.php">
            <div class="tm-logo-icon">T</div>
            <span>TechMatch</span>
        </a>

        <div class="tm-nav-links">
            <a href="catalogo.php" class="tm-nav-link">Catálogo</a>
            <a href="comparar.php" class="tm-nav-link">Comparar</a>
        </div>

        <div class="tm-nav-actions">
            <!-- Estado: no logueado -->
            <div id="nav-sin-sesion">
                <a href="login.php" class="tm-btn tm-btn-ghost tm-btn-sm">Iniciar Sesión</a>
                <a href="registro.php" class="tm-btn tm-btn-primary tm-btn-sm">Registrarse</a>
            </div>

            <!-- Estado: logueado (oculto hasta que JS lo muestre) -->
            <div id="nav-con-sesion" style="display:none;" class="tm-nav-actions">
                <span style="color: var(--tm-text-secondary); font-size: 0.85rem;" id="nav-nombre-usuario"></span>
                <button class="tm-btn tm-btn-ghost tm-btn-sm" onclick="cerrarSesion()">Salir</button>
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
