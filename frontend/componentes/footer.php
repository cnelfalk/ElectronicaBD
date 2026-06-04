<footer class="tm-footer">
    <div class="tm-footer-inner">
        <div class="tm-footer-brand">
            <a class="tm-logo" href="catalogo.php" style="font-size: 1.15rem;">
                <div class="tm-logo-icon" style="width:28px; height:28px; font-size:0.85rem;">T</div>
                <span>TechMatch</span>
            </a>
            <p>Plataforma inteligente de comparación de hardware. Analizamos especificaciones técnicas reales extraídas directamente de los fabricantes para ayudarte a elegir el equipo perfecto.</p>
        </div>

        <div class="tm-footer-col">
            <h4>Plataforma</h4>
            <ul>
                <li><a href="catalogo.php#zona-catalogo">Catálogo</a></li>
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
                <li><a href="catalogo.php?categoria=laptop#zona-catalogo">Laptops</a></li>
                <li><a href="catalogo.php?categoria=cpu#zona-catalogo">Procesadores</a></li>
                <li><a href="catalogo.php?categoria=gpu#zona-catalogo">Placas de Video</a></li>
                <li><a href="catalogo.php?categoria=ram#zona-catalogo">Memoria RAM</a></li>
                <li><a href="catalogo.php?categoria=almacenamiento#zona-catalogo">Almacenamiento</a></li>
            </ul>
        </div>

        <div class="tm-footer-col">
            <h4>Marcas</h4>
            <ul>
                <li><a href="catalogo.php?marca=asus#zona-catalogo">ASUS</a></li>
                <li><a href="catalogo.php?marca=lenovo#zona-catalogo">Lenovo</a></li>
                <li><a href="catalogo.php?marca=intel#zona-catalogo">Intel</a></li>
                <li><a href="catalogo.php?marca=amd#zona-catalogo">AMD</a></li>
                <li><a href="catalogo.php?marca=nvidia#zona-catalogo">NVIDIA</a></li>
            </ul>
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
    </div>
</footer>

<script>
document.addEventListener('DOMContentLoaded', () => {
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
                        
                        // Lo mandamos al catálogo
                        window.location.href = 'catalogo.php'; 
                    }
                });
            }
        }
    }
});
</script>