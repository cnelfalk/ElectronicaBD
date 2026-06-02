<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Detalle de Producto</title>
    <meta name="description" content="Visualizá las especificaciones técnicas completas y precios actualizados de este producto en TechMatch.">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        /* ── Estilos específicos para la vista de detalle ── */
        .tm-detail-container {
            max-width: 960px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }

        .tm-detail-back {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--text-secondary, #aaa);
            text-decoration: none;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
            transition: color 0.2s;
        }
        .tm-detail-back:hover { color: var(--accent, #6c5ce7); }

        .tm-detail-card {
            background: var(--card-bg, #1e1e2e);
            border-radius: 16px;
            border: 1px solid var(--border, #2a2a3e);
            overflow: hidden;
        }

        .tm-detail-hero {
            display: grid;
            grid-template-columns: 340px 1fr;
            gap: 2rem;
            padding: 2rem;
        }
        @media (max-width: 768px) {
            .tm-detail-hero { grid-template-columns: 1fr; }
        }

        .tm-detail-img-wrap {
            background: var(--bg-secondary, #16161e);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            min-height: 260px;
        }
        .tm-detail-img-wrap img {
            max-width: 100%;
            max-height: 280px;
            object-fit: contain;
            border-radius: 8px;
        }

        .tm-detail-info { display: flex; flex-direction: column; gap: 0.8rem; }

        .tm-detail-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            width: fit-content;
        }

        .tm-detail-modelo {
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text-primary, #fff);
            margin: 0;
            line-height: 1.3;
        }

        .tm-detail-marca {
            font-size: 1rem;
            color: var(--text-secondary, #aaa);
            margin: 0;
        }

        /* ── Sección de Specs ── */
        .tm-detail-section {
            padding: 1.5rem 2rem;
            border-top: 1px solid var(--border, #2a2a3e);
        }
        .tm-detail-section h3 {
            font-size: 1.1rem;
            color: var(--text-primary, #fff);
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tm-specs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 0.8rem;
        }

        .tm-spec-item {
            background: var(--bg-secondary, #16161e);
            border-radius: 10px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
        }
        .tm-spec-label {
            font-size: 0.75rem;
            color: var(--text-secondary, #aaa);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .tm-spec-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary, #fff);
        }

        /* ── Tabla de Precios ── */
        .tm-prices-table {
            width: 100%;
            border-collapse: collapse;
        }
        .tm-prices-table th, .tm-prices-table td {
            padding: 0.8rem 1rem;
            text-align: left;
        }
        .tm-prices-table th {
            font-size: 0.75rem;
            color: var(--text-secondary, #aaa);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--border, #2a2a3e);
        }
        .tm-prices-table td {
            font-size: 0.95rem;
            color: var(--text-primary, #fff);
            border-bottom: 1px solid var(--border, #2a2a3e);
        }
        .tm-prices-table tr:last-child td { border-bottom: none; }

        .tm-price-value {
            font-weight: 700;
            color: var(--accent, #6c5ce7);
            font-size: 1.1rem;
        }

        .tm-price-link {
            color: var(--accent, #6c5ce7);
            text-decoration: none;
            font-weight: 500;
            transition: opacity 0.2s;
        }
        .tm-price-link:hover { opacity: 0.8; }

        .tm-price-date {
            font-size: 0.8rem;
            color: var(--text-secondary, #aaa);
        }

        .tm-no-prices {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary, #aaa);
        }

        .tm-detail-actions {
            display: flex;
            gap: 0.8rem;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <div class="tm-detail-container" id="detalleContainer">
        <div class="tm-loading">
            <div class="tm-spinner"></div>
            <p>Cargando detalle del producto...</p>
        </div>
    </div>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script>
    document.addEventListener('DOMContentLoaded', async () => {
        const container = document.getElementById('detalleContainer');
        const params = new URLSearchParams(window.location.search);
        const idProducto = params.get('id');

        if (!idProducto) {
            container.innerHTML = `
                <div class="tm-empty">
                    <div class="tm-empty-icon">⚠️</div>
                    <p>No se especificó un producto. <a href="catalogo.php">Volver al catálogo</a></p>
                </div>
            `;
            return;
        }

        try {
            const resp = await fetch(`${API_URL}/productos/${idProducto}`);
            const data = await resp.json();

            if (!data.success) {
                container.innerHTML = `
                    <div class="tm-empty">
                        <div class="tm-empty-icon">🔍</div>
                        <p>${data.mensaje || 'Producto no encontrado.'} <a href="catalogo.php">Volver al catálogo</a></p>
                    </div>
                `;
                return;
            }

            const { producto, specs, precios } = data.data;

            // Actualizar título de la página
            document.title = `${producto.modelo} — TechMatch`;

            // Badge class por categoría
            const badgeClasses = {
                'CPU': 'tm-badge-cpu',
                'GPU': 'tm-badge-gpu',
                'RAM': 'tm-badge-ram',
                'Laptop': 'tm-badge-laptop',
                'Almacenamiento': 'tm-badge-laptop'
            };
            const badgeClass = badgeClasses[producto.categoria] || 'tm-badge-laptop';

            // Generar HTML de specs según categoría
            let specsHTML = '';
            if (specs) {
                specsHTML = generarSpecsHTML(producto.categoria, specs);
            } else {
                specsHTML = '<p style="color: var(--text-secondary, #aaa);">Las especificaciones técnicas de este producto aún no están disponibles.</p>';
            }

            // Generar HTML de precios
            let preciosHTML = '';
            if (precios && precios.length > 0) {
                preciosHTML = `
                    <table class="tm-prices-table">
                        <thead>
                            <tr>
                                <th>Tienda</th>
                                <th>Precio</th>
                                <th>Enlace</th>
                                <th>Actualizado</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${precios.map(p => `
                                <tr>
                                    <td>${p.nombre_tienda}</td>
                                    <td class="tm-price-value">$${Number(p.precio).toLocaleString('es-AR')}</td>
                                    <td>
                                        ${p.url_producto 
                                            ? `<a href="${p.url_producto}" target="_blank" rel="noopener" class="tm-price-link">Ver en tienda →</a>` 
                                            : '-'}
                                    </td>
                                    <td class="tm-price-date">${p.fec_actualizacion ? new Date(p.fec_actualizacion).toLocaleDateString('es-AR') : '-'}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
            } else {
                preciosHTML = `<div class="tm-no-prices">Este producto aún no tiene precios registrados en tiendas.</div>`;
            }

            // Imagen con ícono por categoría cuando no hay foto
            const iconosCategoria = {
                'CPU': '🔲', 'GPU': '🎮', 'RAM': '💾',
                'Laptop': '💻', 'Almacenamiento': '📀'
            };
            const iconoFallback = iconosCategoria[producto.categoria] || '📦';

            const imgHTML = producto.img_url
                ? `<img src="${producto.img_url}" alt="${producto.modelo}" onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'font-size:3rem;\\'>${iconoFallback}</div>';">`
                : `<div style="font-size:3rem;">${iconoFallback}</div>`;

            container.innerHTML = `
                <a href="catalogo.php" class="tm-detail-back">← Volver al catálogo</a>

                <div class="tm-detail-card">
                    <div class="tm-detail-hero">
                        <div class="tm-detail-img-wrap">
                            ${imgHTML}
                        </div>
                        <div class="tm-detail-info">
                            <span class="tm-card-badge ${badgeClass} tm-detail-badge">${producto.categoria}</span>
                            <h1 class="tm-detail-modelo">${producto.modelo}</h1>
                            <p class="tm-detail-marca">${producto.marca}</p>

                            ${precios && precios.length > 0
                                ? `<p style="margin:0;"><span class="tm-price-value" style="font-size:1.5rem;">$${Number(precios[0].precio).toLocaleString('es-AR')}</span> <span class="tm-price-date">en ${precios[0].nombre_tienda}</span></p>`
                                : ''}

                            <div class="tm-detail-actions">
                                <button class="tm-btn tm-btn-outline tm-btn-sm" onclick="agregarYComparar(${producto.id_producto}, '${producto.categoria}', '${producto.modelo.replace(/'/g, "\\'")}')">
                                    ⚖️ Comparar
                                </button>
                                <button class="tm-btn tm-btn-ghost tm-btn-sm" id="btnFavDetalle" data-id="${producto.id_producto}">
                                    ❤️ Guardar
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="tm-detail-section">
                        <h3>📋 Especificaciones Técnicas</h3>
                        ${specsHTML}
                    </div>

                    <div class="tm-detail-section">
                        <h3>💰 Precios en Tiendas</h3>
                        ${preciosHTML}
                    </div>
                </div>
            `;

            // Inicializar estado del botón favorito
            initFavoritoDetalle(producto.id_producto);

        } catch (error) {
            console.error('Error cargando detalle:', error);
            container.innerHTML = `
                <div class="tm-empty">
                    <div class="tm-empty-icon">⚠️</div>
                    <p>Error al conectar con el servidor. <a href="catalogo.php">Volver al catálogo</a></p>
                </div>
            `;
        }
    });

    // ── Genera el grid de specs según la categoría del producto ──
    function generarSpecsHTML(categoria, specs) {
        let items = [];

        if (categoria === 'Laptop') {
            items = [
                { label: 'Procesador', value: specs.cpu_modelo || '-' },
                { label: 'Gráficos', value: specs.gpu_modelo || '-' },
                { label: 'Memoria RAM', value: `${specs.ram_gb || '-'} GB` },
                { label: 'Almacenamiento', value: `${specs.almacenamiento_gb || '-'} GB` },
                { label: 'Pantalla', value: `${specs.tamanio_pantalla || '-'}"` },
                { label: 'Tasa de Refresco', value: `${specs.tasa_refresco_hz || '-'} Hz` },
                { label: 'Batería', value: `${specs.capacidad_bateria_wh || '-'} Wh` },
                { label: 'Peso', value: `${specs.peso_kg || '-'} kg` },
            ];
        } else if (categoria === 'CPU') {
            items = [
                { label: 'Núcleos', value: specs.nucleos || '-' },
                { label: 'Hilos', value: specs.hilos || '-' },
                { label: 'Frecuencia Base', value: `${specs.frecuencia_base || '-'} GHz` },
                { label: 'Frecuencia Turbo', value: `${specs.frecuencia_turbo || '-'} GHz` },
                { label: 'TDP', value: `${specs.tdp || '-'} W` },
            ];
        } else if (categoria === 'GPU') {
            items = [
                { label: 'VRAM',            value: specs.vram_gb ? `${specs.vram_gb} GB` : '-' },
                { label: 'Tipo de Memoria', value: specs.tipo_memoria || '-' },
                { label: 'TDP',             value: specs.tdp_w   ? `${specs.tdp_w} W`   : '-' },
            ];
        } else if (categoria === 'RAM') {
            items = [
                { label: 'Capacidad',    value: specs.capacidad_gb  ? `${specs.capacidad_gb} GB`   : '-' },
                { label: 'Tipo',         value: specs.tipo_memoria || '-' },
                { label: 'Velocidad',    value: specs.velocidad_mhz ? `${specs.velocidad_mhz} MHz` : '-' },
                { label: 'Latencia CAS', value: specs.latencia      ? `CL${specs.latencia}`        : '-' },
            ];
        } else if (categoria === 'Almacenamiento') {
            items = [
                { label: 'Capacidad',         value: specs.capacidad_gb     ? `${specs.capacidad_gb} GB`       : '-' },
                { label: 'Tipo',              value: specs.tipo_disco || '-' },
                { label: 'Velocidad Lectura', value: specs.velocidad_lectura ? `${specs.velocidad_lectura} MB/s` : '-' },
            ];
        }

        return `
            <div class="tm-specs-grid">
                ${items.map(i => `
                    <div class="tm-spec-item">
                        <span class="tm-spec-label">${i.label}</span>
                        <span class="tm-spec-value">${i.value}</span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // ── Favorito desde detalle ──
    async function initFavoritoDetalle(idProducto) {
        const btn = document.getElementById('btnFavDetalle');
        if (!btn) return;

        const usuarioInfo = localStorage.getItem('techmatch_usuario');
        if (!usuarioInfo) return;

        const usuario = JSON.parse(usuarioInfo);
        try {
            const resp = await fetch(`${API_URL}/favoritos/${usuario.idUsuario}`);
            const data = await resp.json();
            if (data.success) {
                const esFav = data.data.some(f => f.id_producto === idProducto);
                if (esFav) {
                    btn.innerHTML = '❤️ Guardado';
                    btn.classList.add('tm-btn-primary');
                    btn.classList.remove('tm-btn-ghost');
                    btn.dataset.fav = 'true';
                }
            }
        } catch (e) {
            console.error('Error verificando favorito:', e);
        }

        btn.addEventListener('click', async () => {
            if (!localStorage.getItem('techmatch_usuario')) {
                window.location.href = 'login.php?redirect=detalle_producto.php?id=' + idProducto;
                return;
            }
            const usr = JSON.parse(localStorage.getItem('techmatch_usuario'));
            const esFav = btn.dataset.fav === 'true';
            btn.disabled = true;
            btn.innerHTML = '⏳ Procesando...';

            try {
                const url = esFav ? `${API_URL}/favoritos/eliminar` : `${API_URL}/favoritos/agregar`;
                const method = esFav ? 'DELETE' : 'POST';
                const resp = await fetch(url, {
                    method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ idUsuario: usr.idUsuario, idProducto })
                });
                const data = await resp.json();
                if (data.success) {
                    btn.dataset.fav = esFav ? 'false' : 'true';
                    btn.innerHTML = esFav ? '❤️ Guardar' : '❤️ Guardado';
                    btn.classList.toggle('tm-btn-primary');
                    btn.classList.toggle('tm-btn-ghost');
                } else {
                    alert(data.mensaje);
                    btn.innerHTML = esFav ? '❤️ Guardado' : '❤️ Guardar';
                }
            } catch (e) {
                alert('Error al procesar favorito.');
                btn.innerHTML = esFav ? '❤️ Guardado' : '❤️ Guardar';
            }
            btn.disabled = false;
        });
    }

    // ── Agregar a comparación desde detalle ──
    function agregarYComparar(id, categoria, modelo) {
        let items = JSON.parse(sessionStorage.getItem('techmatch_comparar') || '[]');
        
        if (items.length > 0 && items[0].categoria !== categoria) {
            alert(`No podés comparar un producto de categoría ${categoria} con uno de categoría ${items[0].categoria}.`);
            return;
        }
        if (items.length >= 2) {
            alert('Solo podés comparar hasta 2 productos. Andá al catálogo para gestionar la comparación.');
            return;
        }
        if (items.some(i => i.id === String(id))) {
            alert('Este producto ya está en la comparación.');
            return;
        }

        items.push({ id: String(id), categoria, modelo });
        sessionStorage.setItem('techmatch_comparar', JSON.stringify(items));
        
        if (items.length === 2) {
            window.location.href = `comparar.php?idA=${items[0].id}&idB=${items[1].id}`;
        } else {
            alert('Producto agregado a la comparación. Seleccioná otro producto para comparar.');
        }
    }
    </script>
</body>
</html>
