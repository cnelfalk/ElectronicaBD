<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Catálogo de Productos</title>
    <meta name="description" content="Explorá el catálogo completo de TechMatch. Filtrá laptops, procesadores, placas de video y más por categoría y marca.">
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <section class="tm-catalog" id="zona-catalogo" style="padding-top: 2rem;">
        <div class="tm-catalog-header">
            <h2>Catálogo de Productos</h2>
        </div>

        <div class="tm-catalog-layout">
            <aside class="tm-filters">
                <div class="tm-filters-title">Filtros</div>

                <div class="tm-filter-group">
                    <label for="buscarNombre">Buscar producto</label>
                    <input type="text" class="tm-input" id="buscarNombre" placeholder="Ej. Ryzen 5, Vivobook...">
                </div>

                <div class="tm-filter-group">
                    <label for="filtroMarca">Marca</label>
                    <select class="tm-select" id="filtroMarca">
                        <option value="">Todas las marcas</option>
                        <!-- Opciones cargadas dinámicamente por catalogo.js desde la API -->
                    </select>
                </div>

                <div class="tm-filter-group">
                    <label for="filtroCategoria">Categoría</label>
                    <select class="tm-select" id="filtroCategoria">
                        <option value="">Todas</option>
                        <option value="CPU">Procesadores</option>
                        <option value="GPU">Placas de Video</option>
                        <option value="RAM">Memoria RAM</option>
                        <option value="Laptop">Laptops</option>
                        <option value="Almacenamiento">Almacenamiento</option>
                    </select>
                </div>

                <div class="tm-filter-group">
                    <label for="filtroOrdenar">Ordenar por</label>
                    <select class="tm-select" id="filtroOrdenar">
                        <option value="">A–Z (por defecto)</option>
                        <option value="populares">🔥 Más populares</option>
                    </select>
                </div>

                <button class="tm-btn tm-btn-primary tm-btn-w-full" id="btnAplicarFiltros">
                    Aplicar filtros
                </button>
            </aside>

            <div class="tm-product-grid" id="contenedorProductos">
                <div class="tm-loading">
                    <div class="tm-spinner"></div>
                    <p>Cargando catálogo...</p>
                </div>
            </div>
        </div>
    </section>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script src="assets/js/catalogo.js"></script>
</body>
</html>