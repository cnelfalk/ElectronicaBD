<?php
# ═══════════════════════════════════════════════════════════════════════════
# card_producto.php — Componente reutilizable para renderizar tarjetas de producto
# ═══════════════════════════════════════════════════════════════════════════

/**
 * Renderiza una tarjeta de producto de forma consistente y segura.
 *
 * @param array $producto Datos del producto (id_producto, modelo, marca, categoria, img_url, precio, etc.).
 * @param bool $mostrarAcciones Define si se renderizan los botones de comparar y favorito.
 */
function render_card_producto($producto, $mostrarAcciones = true) {
    // Sanitizar datos del producto para prevenir ataques XSS
    $id = intval($producto['id_producto']);
    $modelo = htmlspecialchars($producto['modelo'] ?? $producto['modelo_producto'] ?? '', ENT_QUOTES, 'UTF-8');
    $marca = htmlspecialchars($producto['marca'] ?? $producto['nombre_marca'] ?? '', ENT_QUOTES, 'UTF-8');
    $categoria = htmlspecialchars($producto['categoria'] ?? $producto['nombre_categoria'] ?? '', ENT_QUOTES, 'UTF-8');
    $imgUrl = htmlspecialchars($producto['img_url'] ?? '', ENT_QUOTES, 'UTF-8');
    $precio = isset($producto['precio']) ? floatval($producto['precio']) : null;
    
    // Asignación de clase CSS para el badge según la categoría
    $badgeClasses = [
        'CPU' => 'tm-badge-cpu',
        'GPU' => 'tm-badge-gpu',
        'RAM' => 'tm-badge-ram',
        'Laptop' => 'tm-badge-laptop',
        'Almacenamiento' => 'tm-badge-storage'
    ];
    $badgeClass = $badgeClasses[$categoria] ?? 'tm-badge-laptop';
    
    // Obtener inicial para el placeholder de la tarjeta
    $inicialMarca = $marca ? strtoupper($marca[0]) : '?';
    ?>
    <div class="tm-card" id="product-card-<?php echo $id; ?>">
        <div class="tm-card-img">
            <?php if ($imgUrl): ?>
                <img src="<?php echo $imgUrl; ?>" alt="<?php echo $modelo; ?>" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <?php endif; ?>
            <div class="tm-card-placeholder" style="<?php echo $imgUrl ? 'display:none;' : ''; ?>">
                <span class="tm-card-placeholder-letter"><?php echo $inicialMarca; ?></span>
                <span class="tm-card-placeholder-brand"><?php echo $marca ?: 'Sin marca'; ?></span>
            </div>
        </div>
        <div class="tm-card-body">
            <span class="tm-card-badge <?php echo $badgeClass; ?>"><?php echo $categoria; ?></span>
            <h3 class="tm-card-title" title="<?php echo $modelo; ?>">
                <a href="detalle_producto.php?id=<?php echo $id; ?>" class="tm-card-link">
                    <?php echo $modelo; ?>
                </a>
            </h3>
            <p class="tm-card-brand"><?php echo $marca; ?></p>
            
            <?php if ($precio !== null && $precio > 0): ?>
                <p class="tm-card-price">
                    <?php echo '$ ' . number_format($precio, 2, ',', '.'); ?>
                </p>
            <?php endif; ?>
            
            <?php if ($mostrarAcciones): ?>
                <div class="tm-card-actions">
                    <button class="tm-btn tm-btn-outline tm-btn-sm" 
                            data-id="<?php echo $id; ?>" 
                            data-categoria="<?php echo $categoria; ?>" 
                            data-modelo="<?php echo $modelo; ?>" 
                            onclick="agregarComparar(this)">
                        ⚖️ Comparar
                    </button>
                    <button class="tm-btn tm-btn-ghost tm-btn-sm btn-favorito" 
                            data-id="<?php echo $id; ?>">
                        ❤️ Guardar
                    </button>
                </div>
            <?php endif; ?>
        </div>
    </div>
    <?php
}
?>
