<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis Comparaciones — TechMatch</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <section class="tm-catalog" style="padding-top: 3rem; padding-bottom: 5rem; min-height: 70vh;">
        <div class="tm-catalog-header" style="max-width: 1200px; margin: 0 auto 2rem auto; padding: 0 1rem;">
            <h2 style="font-size: 2.2rem; font-weight: 800; margin: 0;">Mis Comparaciones Guardadas</h2>
            <p style="color: var(--tm-text-secondary); margin: 0.35rem 0 0 0; font-size: 1rem;">Historial y acceso directo a tus comparaciones técnicas guardadas.</p>
        </div>

        <div class="tm-product-grid" id="contenedorComparaciones" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
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