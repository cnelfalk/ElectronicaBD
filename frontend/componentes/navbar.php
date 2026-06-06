<script src="assets/js/alertas.js"></script>

<style>
/* ── Estilos responsivos del Menú Móvil (Hamburguesa) ── */
.tm-menu-toggle {
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 24px;
    height: 18px;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 1001;
}

.tm-menu-toggle span {
    width: 100%;
    height: 2px;
    background-color: var(--tm-text-primary, #f1f5f9);
    border-radius: 2px;
    transition: var(--tm-transition-fast, all 0.15s ease);
}

.tm-mobile-menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: rgba(10, 14, 23, 0.96);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--tm-border, rgba(148, 163, 184, 0.1));
    padding: 1.25rem 1.5rem;
    z-index: 999;
    opacity: 0;
    transform: translateY(-10px);
    transition: opacity 0.25s ease, transform 0.25s ease;
    pointer-events: none;
}

.tm-mobile-menu.active {
    display: block;
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
}

.tm-mobile-menu-links {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    width: 100%;
}

.tm-mobile-link {
    display: block;
    padding: 0.75rem 1rem;
    color: var(--tm-text-secondary, #94a3b8) !important;
    font-size: 0.95rem;
    font-weight: 500;
    border-radius: var(--tm-radius-sm, 8px);
    transition: var(--tm-transition-fast, all 0.15s ease);
    text-decoration: none;
}

.tm-mobile-link:hover {
    color: var(--tm-text-primary, #f1f5f9) !important;
    background: rgba(148, 163, 184, 0.08);
}

.tm-mobile-btn-primary {
    background: var(--tm-accent-gradient);
    color: var(--tm-bg-primary, #0a0e17) !important;
    text-align: center;
    font-weight: 600;
    margin-top: 0.5rem;
}

.tm-mobile-btn-primary:hover {
    background: var(--tm-accent-gradient-hover);
    box-shadow: 0 4px 12px rgba(34, 211, 238, 0.2);
}

/* Ocultar elementos de escritorio y mostrar menú móvil en pantallas menores a 768px */
@media (max-width: 768px) {
    .tm-nav-links, .tm-nav-actions {
        display: none !important;
    }
    
    .tm-menu-toggle {
        display: flex;
    }

    /* Animación del ícono de hamburguesa que se convierte en X */
    .tm-menu-toggle.active span:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
    }
    
    .tm-menu-toggle.active span:nth-child(2) {
        opacity: 0;
    }
    
    .tm-menu-toggle.active span:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
    }
}
</style>

<nav class="tm-navbar">
    <div class="tm-navbar-inner">
        <a class="tm-logo" href="index.php">
            <div class="tm-logo-icon">T</div>
            <span>TechMatch</span>
        </a>

        <!-- Enlaces para Escritorio -->
        <div class="tm-nav-links">
            <a href="index.php" class="tm-nav-link">Inicio</a>
            <a href="catalogo.php" class="tm-nav-link">Catálogo</a>
        </div>

        <!-- Acciones para Escritorio -->
        <div class="tm-nav-actions">
            <div id="nav-sin-sesion">
                <a href="login.php" class="tm-btn tm-btn-ghost tm-btn-sm">Iniciar sesión</a>
                <a href="registro.php" class="tm-btn tm-btn-primary tm-btn-sm">Registrarse</a>
            </div>

            <div id="nav-con-sesion" style="display:none;" class="tm-nav-actions">
                <a href="favoritos.php" class="tm-nav-link" style="font-size: 0.85rem;">❤️ Mis favoritos</a>
                <a href="comparaciones_guardadas.php" class="tm-nav-link" style="font-size: 0.85rem; margin-right: 0.5rem;">⚖️ Mis comparaciones</a>
                <span style="color: var(--tm-text-secondary); font-size: 0.85rem;" id="nav-nombre-usuario"></span>
                <button class="tm-btn tm-btn-ghost tm-btn-sm" onclick="cerrarSesion()">Cerrar sesión</button>
            </div>
        </div>

        <!-- Botón de Hamburguesa (Móvil) -->
        <button class="tm-menu-toggle" id="menuToggle" aria-label="Abrir menú">
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>

    <!-- Menú Desplegable (Móvil) -->
    <div class="tm-mobile-menu" id="mobileMenu">
        <div class="tm-mobile-menu-links">
            <a href="index.php" class="tm-mobile-link">Inicio</a>
            <a href="catalogo.php" class="tm-mobile-link">Catálogo</a>
            
            <!-- Opciones para móvil sin sesión -->
            <div id="mobile-sin-sesion">
                <a href="login.php" class="tm-mobile-link">Iniciar sesión</a>
                <a href="registro.php" class="tm-mobile-link tm-mobile-btn-primary">Registrarse</a>
            </div>
            
            <!-- Opciones para móvil con sesión -->
            <div id="mobile-con-sesion" style="display:none; flex-direction: column; width: 100%;">
                <a href="favoritos.php" class="tm-mobile-link">❤️ Mis favoritos</a>
                <a href="comparaciones_guardadas.php" class="tm-mobile-link">⚖️ Mis comparaciones</a>
                <span style="color: var(--tm-text-secondary); font-size: 0.85rem; padding: 0.75rem 1rem; border-top: 1px solid var(--tm-border); display: block;" id="mobile-nombre-usuario"></span>
                <button class="tm-mobile-link" onclick="cerrarSesion()" style="background: transparent; border: none; text-align: left; cursor: pointer; font-family: inherit; font-size: inherit; color: inherit; width: 100%;">Cerrar sesión</button>
            </div>
        </div>
    </div>
</nav>

<script>
    (function () {
        const datos = localStorage.getItem('techmatch_usuario');
        if (datos) {
            const usuario = JSON.parse(datos);
            // Mostrar vistas de sesión en Escritorio
            document.getElementById('nav-sin-sesion').style.display = 'none';
            document.getElementById('nav-con-sesion').style.display = 'flex';
            document.getElementById('nav-nombre-usuario').textContent = 'Hola, ' + usuario.nombreUsuario;

            // Mostrar vistas de sesión en Móvil
            document.getElementById('mobile-sin-sesion').style.display = 'none';
            document.getElementById('mobile-con-sesion').style.display = 'flex';
            document.getElementById('mobile-nombre-usuario').textContent = 'Hola, ' + usuario.nombreUsuario;
        }
    })();

    // Lógica para alternar el menú desplegable en móvil
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }

    async function cerrarSesion() {
        const confirmado = await mostrarConfirmacion("¿Estás seguro de que querés cerrar sesión?");
        
        if (confirmado) {
            localStorage.removeItem('techmatch_usuario');
            try {
                await fetch('utils/clear_session.php');
            } catch(e) {}
            window.location.href = 'index.php';
        }
    }
</script>
