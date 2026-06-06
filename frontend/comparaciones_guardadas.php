<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis comparaciones — TechMatch</title>
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <section class="tm-catalog" style="padding-top: 3rem; padding-bottom: 5rem; min-height: 70vh;">
        <div class="tm-catalog-header" style="max-width: 1200px; margin: 0 auto 2rem auto; padding: 0 1rem; display: flex; flex-direction: column; align-items: flex-start; gap: 0.25rem;">
            <h2 class="tm-page-title">Mis comparaciones guardadas</h2>
            <p class="tm-page-subtitle">Historial y acceso directo a tus comparaciones técnicas guardadas.</p>
        </div>

        <div class="tm-product-grid tm-grid-comparaciones" id="contenedorComparaciones" style="gap: 1.5rem; max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
            <div class="tm-loading" style="grid-column: 1 / -1; text-align: center; padding: 4rem 0;">
                <div class="tm-spinner"></div>
                <p style="margin-top: 1rem; color: var(--tm-text-secondary);">Cargando tu historial...</p>
            </div>
        </div>
    </section>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js?v=<?php echo time(); ?>"></script>
    <script src="assets/js/comparaciones_guardadas.js?v=<?php echo time(); ?>"></script>
</body>
</html>