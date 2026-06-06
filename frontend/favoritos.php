<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis favoritos — TechMatch</title>
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <section class="tm-catalog">
        <div class="tm-catalog-header">
            <h2 class="tm-page-title">Mis favoritos</h2>
        </div>

        <div class="tm-product-grid" id="contenedorFavoritos">
            <div class="tm-loading">
                <div class="tm-spinner"></div>
                <p>Cargando favoritos...</p>
            </div>
        </div>
    </section>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script src="assets/js/favoritos.js"></script>
</body>
</html>