<script src="assets/js/alertas.js"></script>
<nav class="tm-navbar">
    <div class="tm-navbar-inner">
        <a class="tm-logo" href="catalogo.php">
            <div class="tm-logo-icon">T</div>
            <span>TechMatch</span>
        </a>

        <div class="tm-nav-links">
            <a href="catalogo.php#catalogo" class="tm-nav-link">Catálogo</a>
            <a href="#" class="tm-nav-link" onclick="return irACompararDesdeNav(event)">Comparar</a>
        </div>

        <div class="tm-nav-actions">
            <!-- Estado: no logueado -->
            <div id="nav-sin-sesion">
                <a href="login.php" class="tm-btn tm-btn-ghost tm-btn-sm">Iniciar Sesión</a>
                <a href="registro.php" class="tm-btn tm-btn-primary tm-btn-sm">Registrarse</a>
            </div>

            <!-- Estado: logueado (oculto hasta que JS lo muestre) -->
            <div id="nav-con-sesion" style="display:none;" class="tm-nav-actions">
                <a href="favoritos.php" class="tm-nav-link" style="font-size: 0.85rem;">❤️ Mis Favoritos</a>
                <a href="comparaciones_guardadas.php" class="tm-nav-link" style="font-size: 0.85rem;">⚖️ Mis Comparaciones</a>
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

    async function cerrarSesion() {
        localStorage.removeItem('techmatch_usuario');
        try {
            await fetch('utils/clear_session.php');
        } catch(e) {}
        window.location.href = 'catalogo.php';
    }

    // irACompararDesdeNav - Valida que haya 2 productos seleccionados antes de redirigir a comparar.php
    function irACompararDesdeNav(event) {
        event.preventDefault();
        const items = JSON.parse(sessionStorage.getItem('techmatch_comparar') || '[]');
        
        if (items.length === 2) {
            window.location.href = `comparar.php?idA=${items[0].id}&idB=${items[1].id}`;
        } else if (items.length === 1) {
            alert('Seleccioná un producto más desde el catálogo para poder comparar.');
        } else {
            alert('Primero seleccioná 2 productos desde el catálogo para compararlos.');
        }
        return false;
    }
</script>

