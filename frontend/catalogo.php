<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Comparador Inteligente de Hardware</title>
    <meta name="description" content="Compará laptops, procesadores y componentes con datos reales de fabricantes. TechMatch te ayuda a encontrar el hardware perfecto para tu perfil de uso.">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <!-- ══════════════════════════════════════
         HERO — Explicación de TechMatch
         ══════════════════════════════════════ -->
    <section class="tm-hero">
        <div class="tm-hero-content">
            <div class="tm-hero-badge">
                ⚡ Datos reales de fabricantes
            </div>
            <h1>
                Encontrá tu hardware ideal con
                <span class="tm-gradient-text">TechMatch</span>
            </h1>
            <p>
                Comparamos laptops y componentes usando especificaciones técnicas reales
                extraídas directamente de ASUS, Lenovo, Intel y AMD.
                Sin datos inventados, sin marketing — solo specs reales y precios actualizados.
            </p>
            <div class="tm-hero-actions">
                <a href="#catalogo" class="tm-btn tm-btn-primary tm-btn-lg">
                    🔍 Explorar Catálogo
                </a>
                <a href="comparar.php" class="tm-btn tm-btn-ghost tm-btn-lg">
                    ⚖️ Comparar Productos
                </a>
            </div>

            <div class="tm-features-row">
                <div class="tm-feature-pill">
                    <span class="tm-feature-icon">🔬</span>
                    <div class="tm-feature-text">
                        <strong>Specs Reales</strong>
                        Directo de fabricantes
                    </div>
                </div>
                <div class="tm-feature-pill">
                    <span class="tm-feature-icon">💰</span>
                    <div class="tm-feature-text">
                        <strong>Precios Actualizados</strong>
                        MercadoLibre y más
                    </div>
                </div>
                <div class="tm-feature-pill">
                    <span class="tm-feature-icon">📊</span>
                    <div class="tm-feature-text">
                        <strong>Comparación Inteligente</strong>
                        Por perfil de uso
                    </div>
                </div>
            </div>
        </div>
    </section>

    <hr class="tm-section-divider">

    <!-- ══════════════════════════════════════
         CATÁLOGO DE PRODUCTOS
         ══════════════════════════════════════ -->
    <section class="tm-catalog" id="catalogo">
        <div class="tm-catalog-header">
            <h2>Catálogo de Productos</h2>
        </div>

        <div class="tm-catalog-layout">
            <!-- Panel de Filtros -->
            <aside class="tm-filters">
                <div class="tm-filters-title">Filtros</div>

                <div class="tm-filter-group">
                    <label for="buscarNombre">Buscar producto</label>
                    <input type="text" class="tm-input" id="buscarNombre" placeholder="Ej. Ryzen 5, Vivobook...">
                </div>

                <div class="tm-filter-group">
                    <label for="filtroCategoria">Categoría</label>
                    <select class="tm-select" id="filtroCategoria">
                        <option value="">Todas</option>
                        <option value="CPU">Procesadores</option>
                        <option value="GPU">Placas de Video</option>
                        <option value="RAM">Memoria RAM</option>
                        <option value="Laptop">Laptops</option>
                    </select>
                </div>

                <div class="tm-filter-group">
                    <label for="filtroPerfil">Perfil de Uso</label>
                    <select class="tm-select" id="filtroPerfil">
                        <option value="">Cualquiera</option>
                        <option value="Gaming">Gaming</option>
                        <option value="Ofimatica">Ofimática</option>
                        <option value="Diseño">Diseño</option>
                        <option value="Desarrollo">Desarrollo de Software</option>
                    </select>
                </div>

                <button class="tm-btn tm-btn-primary tm-btn-w-full" id="btnAplicarFiltros">
                    Aplicar Filtros
                </button>
            </aside>

            <!-- Grilla de Productos -->
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