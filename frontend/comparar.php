<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Comparar Hardware</title>
    <meta name="description" content="Comparación técnica detallada y recomendación inteligente de hardware según perfiles de uso.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <section class="tm-container" style="padding-top: 3rem; padding-bottom: 4rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800;">Comparación de Hardware</h1>
                <p style="margin: 0.25rem 0 0; color: var(--tm-text-secondary);">Análisis detallado de características y compatibilidad de perfiles de uso.</p>
            </div>
            
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <label for="perfilUso" style="font-weight: 600; font-size: 0.9rem; color: var(--tm-text-secondary);">Perfil de Uso:</label>
                <select class="tm-select" id="perfilUso" style="min-width: 220px; margin: 0;">
                    <option value="Uso General">Uso General</option>
                    <option value="Gaming">Gaming</option>
                    <option value="Diseño">Diseño y Edición</option>
                    <option value="Desarrollo de Software">Desarrollo de Software</option>
                    <option value="Ofimatica">Ofimática / Trabajo Diario</option>
                </select>
            </div>
        </div>

        <div id="comparacionCargando" class="tm-loading">
            <div class="tm-spinner"></div>
            <p>Generando recomendación inteligente...</p>
        </div>

        <div id="comparacionError" class="tm-empty" style="display: none;">
            <div class="tm-empty-icon">⚠️</div>
            <p id="errorMensaje">Ocurrió un error al cargar la comparación.</p>
            <a href="catalogo.php" class="tm-btn tm-btn-primary" style="margin-top: 1rem;">Volver al Catálogo</a>
        </div>

        <div id="comparacionContenido" style="display: none;">
            <!-- Ganador / Recomendación inteligente -->
            <div class="tm-winner-card">
                <span class="tm-winner-badge">Recomendado</span>
                <h2 style="margin: 0 0 0.5rem; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; color: var(--tm-text-muted);">El Veredicto de TechMatch</h2>
                <div class="tm-winner-title" id="ganadorNombre">Nombre del Ganador</div>
                <p class="tm-winner-motivo" id="ganadorMotivo">Justificación de la recomendación basada en el perfil de uso seleccionado.</p>
            </div>

            <!-- Botón para guardar comparación -->
            <div style="margin-top: -1rem; margin-bottom: 2.5rem; display: flex; justify-content: center;">
                <button id="btnGuardarComparacion" class="tm-btn tm-btn-primary" style="display: none; align-items: center; gap: 0.5rem; font-size: 0.9rem; padding: 0.75rem 2rem; border-radius: 8px;">
                    💾 Guardar Comparación
                </button>
            </div>

            <div class="tm-compare-grid">
                <!-- Tabla Side-by-Side -->
                <div>
                    <h2 style="font-size: 1.25rem; margin-bottom: 0.75rem; color: var(--tm-text-primary);">Especificaciones Técnicas</h2>
                    <div class="tm-compare-table-wrapper">
                        <table class="tm-compare-table">
                            <thead>
                                <tr>
                                    <th>Característica</th>
                                    <th id="nombreProductoA">Producto A</th>
                                    <th id="nombreProductoB">Producto B</th>
                                </tr>
                            </thead>
                            <tbody id="tablaEspecificaciones">
                                <!-- Filas dinámicas -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Desglose de Precios en Tiendas -->
                <div>
                    <h2 style="font-size: 1.25rem; margin-bottom: 0.75rem; color: var(--tm-text-primary);">Precios y Tiendas</h2>
                    <div class="tm-prices-comparison">
                        <div class="tm-prices-card">
                            <h3 id="precioTituloA">Tiendas Producto A</h3>
                            <div id="preciosListaA">
                                <!-- Precios dinámicos -->
                            </div>
                        </div>
                        <div class="tm-prices-card">
                            <h3 id="precioTituloB">Tiendas Producto B</h3>
                            <div id="preciosListaB">
                                <!-- Precios dinámicos -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 2.5rem; display: flex; justify-content: center;">
                <a href="catalogo.php" class="tm-btn tm-btn-ghost">
                    ← Volver al Catálogo
                </a>
            </div>
        </div>
    </section>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js?v=<?php echo time(); ?>"></script>
    <script src="assets/js/comparacion.js?v=<?php echo time(); ?>"></script>
</body>
</html>
