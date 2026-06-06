<footer class="tm-footer">
    <div class="tm-footer-inner">
        <div class="tm-footer-brand">
            <a class="tm-logo" href="index.php" style="font-size: 1.15rem;">
                <div class="tm-logo-icon" style="width:28px; height:28px; font-size:0.85rem;">T</div>
                <span>TechMatch</span>
            </a>
            <p>Plataforma inteligente de comparación de hardware. Analizamos especificaciones técnicas reales extraídas directamente de los fabricantes para ayudarte a elegir el equipo perfecto.</p>
        </div>

        <div class="tm-footer-col">
            <h4>Plataforma</h4>
            <ul>
                <li><a href="catalogo.php">Catálogo</a></li>
                <li><a href="comparar.php">Comparador</a></li>
                <li><a href="registro.php" id="linkCuentaFooter">Crear Cuenta</a></li>
                <li><a href="login.php" id="linkSesionFooter">Iniciar Sesión</a></li>
                <li id="itemCerrarSesionFooter" style="display: none;">
                    <a href="#" id="linkCerrarSesionFooter">Cerrar Sesión</a>
                </li>
            </ul>
        </div>

        <div class="tm-footer-col">
            <h4>Categorías</h4>
            <ul>
                <li><a href="catalogo.php?categoria=Laptop#zona-catalogo">Laptops</a></li>
                <li><a href="catalogo.php?categoria=CPU#zona-catalogo">Procesadores</a></li>
                <li><a href="catalogo.php?categoria=GPU#zona-catalogo">Placas de Video</a></li>
                <li><a href="catalogo.php?categoria=RAM#zona-catalogo">Memoria RAM</a></li>
                <li><a href="catalogo.php?categoria=Almacenamiento#zona-catalogo">Almacenamiento</a></li>
            </ul>
        </div>

        <div class="tm-footer-col">
            <h4>Marcas</h4>
            <div style="display: flex; gap: 30px;">
                <ul style="margin: 0; padding: 0;">
                    <li><a href="catalogo.php?marca=asus#zona-catalogo">ASUS</a></li>
                    <li><a href="catalogo.php?marca=lenovo#zona-catalogo">Lenovo</a></li>
                    <li><a href="catalogo.php?marca=intel#zona-catalogo">Intel</a></li>
                    <li><a href="catalogo.php?marca=amd#zona-catalogo">AMD</a></li>
                </ul>
                <ul style="margin: 0; padding: 0;">
                    <li><a href="catalogo.php?marca=nvidia#zona-catalogo">NVIDIA</a></li>
                    <li><a href="catalogo.php?marca=corsair#zona-catalogo">Corsair</a></li>
                    <li><a href="catalogo.php?marca=kingston#zona-catalogo">Kingston</a></li>
                    <li><a href="catalogo.php?marca=western%20digital#zona-catalogo">Western Digital</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="tm-footer-bottom">
        <div class="tm-footer-team" style="margin-bottom: 15px; font-size: 0.9rem; color: #6c757d;">
            <p><strong>Equipo de Desarrollo:</strong> Chiacchio, Matias Daniel | Gomez, Lucas Ivan | Mansilla, Fabrizio Manuel | Ramos, Ludmila Sofia</p>
        </div>

        <p>&copy; <?php echo date('Y'); ?> TechMatch — Proyecto académico de comparación de hardware.</p>
        <div class="tm-footer-tech">
            <span class="tm-tech-badge">PHP</span>
            <span class="tm-tech-badge">Flask</span>
            <span class="tm-tech-badge">MySQL</span>
            <span class="tm-tech-badge">Selenium</span>
    </div>
</footer>

<!-- Botón Regresar al tope -->
<button id="btnBackToTop" class="tm-back-to-top" aria-label="Regresar al tope de la página">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</button>

<script>
// Función global para alternar la visibilidad de la contraseña
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;
    if (input.type === 'password') {
        input.type = 'text';
        btn.classList.add('visible-pass');
    } else {
        input.type = 'password';
        btn.classList.remove('visible-pass');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Lógica para el botón "Regresar al tope"
    const btnBackToTop = document.getElementById('btnBackToTop');
    if (btnBackToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                btnBackToTop.classList.add('visible');
            } else {
                btnBackToTop.classList.remove('visible');
            }
        });

        btnBackToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Capturamos todos los enlaces dinámicos de la columna Plataforma
    const linkCuentaFooter = document.getElementById('linkCuentaFooter');
    const linkSesionFooter = document.getElementById('linkSesionFooter');
    const itemCerrarSesionFooter = document.getElementById('itemCerrarSesionFooter');
    const linkCerrarSesionFooter = document.getElementById('linkCerrarSesionFooter');
    
    if (linkCuentaFooter && linkSesionFooter) {
        // Leemos si hay una sesión activa guardada en el navegador
        const usuarioInfo = localStorage.getItem('techmatch_usuario');
        
        if (usuarioInfo) {
            // 1. Mutamos los botones existentes porque el usuario ESTÁ registrado
            linkCuentaFooter.href = "favoritos.php";
            linkCuentaFooter.innerHTML = "Mis Favoritos";
            
            linkSesionFooter.href = "comparaciones_guardadas.php";
            linkSesionFooter.innerHTML = "Mis Comparaciones";
            
            // 2. Mostramos y activamos el botón de Cerrar Sesión
            if (itemCerrarSesionFooter && linkCerrarSesionFooter) {
                itemCerrarSesionFooter.style.display = 'block';
                
                linkCerrarSesionFooter.addEventListener('click', async (e) => {
                    e.preventDefault(); // Evita el salto molesto hacia arriba
                    
                    // Disparamos el modal personalizado de TechMatch
                    const confirmado = await mostrarConfirmacion("¿Estás seguro de que querés cerrar sesión?");
                    
                    if (confirmado) {
                        // Borramos datos del cliente
                        localStorage.removeItem('techmatch_usuario');
                        
                        // Avisamos al backend PHP que limpie la sesión
                        try {
                            await fetch('utils/clear_session.php');
                        } catch(error) {
                            console.error("Error al limpiar sesión:", error);
                        }
                        
                        // Lo mandamos al inicio
                        window.location.href = 'index.php'; 
                    }
                });
            }
        }
    }
});
</script>