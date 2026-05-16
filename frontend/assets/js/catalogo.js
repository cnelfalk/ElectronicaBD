document.addEventListener('DOMContentLoaded', () => {
    // Referencias a los elementos del DOM
    const contenedorProductos = document.getElementById('contenedorProductos');
    const btnAplicarFiltros = document.getElementById('btnAplicarFiltros');
    const filtroCategoria = document.getElementById('filtroCategoria');
    const filtroPerfil = document.getElementById('filtroPerfil');
    const buscarNombre = document.getElementById('buscarNombre');

    // Función principal para cargar productos
    async function cargarProductos() {
        // Mostrar estado de carga
        contenedorProductos.innerHTML = `
            <div class="tm-loading">
                <div class="tm-spinner"></div>
                <p>Cargando catálogo...</p>
            </div>
        `;

        // Construir la URL con los parámetros de filtro
        const params = new URLSearchParams();
        if (filtroCategoria.value) params.append('categoria', filtroCategoria.value);
        if (filtroPerfil.value) params.append('perfil', filtroPerfil.value);
        if (buscarNombre.value) params.append('busqueda', buscarNombre.value);

        const urlConFiltros = `${API_URL}/productos?${params.toString()}`;

        try {
            const respuesta = await fetch(urlConFiltros);

            if (!respuesta.ok) {
                throw new Error(`Error HTTP: ${respuesta.status}`);
            }

            const datosJson = await respuesta.json();

            if (datosJson.success) {
                renderizarProductos(datosJson.data);
            } else {
                mostrarError(datosJson.mensaje);
            }

        } catch (error) {
            console.error('Error al conectar con la API:', error);
            mostrarError('No se pudo conectar con el servidor. Verificá que Flask esté corriendo en el puerto 5000.');
        }
    }

    // Función para dibujar las tarjetas en el HTML
    function renderizarProductos(productos) {
        contenedorProductos.innerHTML = '';

        if (productos.length === 0) {
            contenedorProductos.innerHTML = `
                <div class="tm-empty">
                    <div class="tm-empty-icon">🔍</div>
                    <p>No se encontraron productos con esos filtros.</p>
                </div>
            `;
            return;
        }

        productos.forEach(producto => {
            const imgSrc = producto.img_url || '';
            const badgeClass = obtenerBadgeClass(producto.categoria);

            const cardHTML = `
                <div class="tm-card">
                    <div class="tm-card-img">
                        ${imgSrc
                            ? `<img src="${imgSrc}" alt="${producto.modelo}" 
                                    onerror="this.style.display='none'; this.parentElement.innerHTML = generarPlaceholder('${producto.marca}');">`
                            : generarPlaceholder(producto.marca)
                        }
                    </div>
                    <div class="tm-card-body">
                        <span class="tm-card-badge ${badgeClass}">${producto.categoria}</span>
                        <h3 class="tm-card-title" title="${producto.modelo}">${producto.modelo}</h3>
                        <p class="tm-card-brand">${producto.marca}</p>
                        <div class="tm-card-actions">
                            <button class="tm-btn tm-btn-outline tm-btn-sm" data-id="${producto.id_producto}" onclick="agregarComparar(this)">
                                ⚖️ Comparar
                            </button>
                            <button class="tm-btn tm-btn-ghost tm-btn-sm" data-id="${producto.id_producto}" onclick="guardarFavorito(this)">
                                ❤️ Guardar
                            </button>
                        </div>
                    </div>
                </div>
            `;
            contenedorProductos.insertAdjacentHTML('beforeend', cardHTML);
        });
    }

    // Clase CSS del badge según la categoría
    function obtenerBadgeClass(categoria) {
        const clases = {
            'CPU': 'tm-badge-cpu',
            'GPU': 'tm-badge-gpu',
            'RAM': 'tm-badge-ram',
            'Laptop': 'tm-badge-laptop'
        };
        return clases[categoria] || 'tm-badge-laptop';
    }

    // Función para mostrar mensajes de error
    function mostrarError(mensaje) {
        contenedorProductos.innerHTML = `
            <div class="tm-empty">
                <div class="tm-empty-icon">⚠️</div>
                <p>${mensaje}</p>
            </div>
        `;
    }

    // --- Event Listeners ---
    cargarProductos();
    btnAplicarFiltros.addEventListener('click', cargarProductos);
    buscarNombre.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') cargarProductos();
    });
});

// Generar placeholder visual cuando no hay imagen
function generarPlaceholder(marca) {
    const inicial = marca ? marca[0].toUpperCase() : '?';
    return `<div class="tm-card-placeholder">
                <span class="tm-card-placeholder-letter">${inicial}</span>
                <span class="tm-card-placeholder-brand">${marca || 'Sin marca'}</span>
            </div>`;
}

// Agregar producto a comparación
function agregarComparar(btn) {
    const idProducto = btn.dataset.id;
    // TODO: Implementar lógica de comparación (Fase 5)
    btn.innerHTML = '✅ Agregado';
    btn.disabled = true;
    btn.style.opacity = '0.6';
}

// Guardar producto como favorito
function guardarFavorito(btn) {
    const usuario = localStorage.getItem('techmatch_usuario');

    if (!usuario) {
        window.location.href = 'login.php?redirect=catalogo.php';
        return;
    }

    // TODO: Conectar con endpoint de favoritos (Fase 5)
    btn.innerHTML = '✅ Guardado';
    btn.disabled = true;
    btn.style.opacity = '0.6';
}