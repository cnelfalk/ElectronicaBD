<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch - Comparador de Hardware</title>
    <!-- CSS de Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Estilos personalizados -->
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <div class="container mt-4">
        <div class="row">
            <!-- Columna Izquierda: Panel de Filtros (RF2.3) -->
            <div class="col-md-3">
                <div class="card mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Filtros Avanzados</h5>
                    </div>
                    <div class="card-body">
                        <!-- Buscador por Nombre (RF2.1) -->
                        <div class="mb-3">
                            <label for="buscarNombre" class="form-label">Buscar producto</label>
                            <input type="text" class="form-control" id="buscarNombre" placeholder="Ej. Ryzen 5...">
                        </div>

                        <!-- Filtro por Categoría -->
                        <div class="mb-3">
                            <label class="form-label">Categoría</label>
                            <select class="form-select" id="filtroCategoria">
                                <option value="">Todas</option>
                                <option value="CPU">Procesadores</option>
                                <option value="GPU">Placas de Video</option>
                                <option value="RAM">Memoria RAM</option>
                                <option value="Laptop">Laptops</option>
                            </select>
                        </div>

                        <!-- Filtro por Perfil de Uso (RF2.2) -->
                        <div class="mb-3">
                            <label class="form-label">Perfil de Uso</label>
                            <select class="form-select" id="filtroPerfil">
                                <option value="">Cualquiera</option>
                                <option value="Gaming">Gaming</option>
                                <option value="Ofimatica">Ofimática</option>
                                <option value="Diseño">Diseño</option>
                                <option value="Desarrollo">Desarrollo de Software</option>
                            </select>
                        </div>

                        <button class="btn btn-primary w-100" id="btnAplicarFiltros">Aplicar Filtros</button>
                    </div>
                </div>
            </div>

            <!-- Columna Derecha: Grilla de Productos -->
            <div class="col-md-9">
                <h2 class="mb-4">Catálogo de Productos</h2>
                
                <!-- Aquí se inyectarán los productos desde JavaScript -->
                <div class="row" id="contenedorProductos">
                    <!-- Ejemplo de cómo se verá un producto (esto lo generará JS luego) -->
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <div class="card-body text-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Cargando...</span>
                                </div>
                                <p class="mt-2">Cargando catálogo...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Script principal -->
    <script src="assets/js/catalogo.js"></script>
</body>
</html>