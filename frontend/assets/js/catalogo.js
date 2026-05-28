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

        // Buscar los favoritos del usuario si está logueado antes de renderizar
        let favoritosIds = [];
        const usuarioInfo = localStorage.getItem('techmatch_usuario');
        if (usuarioInfo) {
            const usuario = JSON.parse(usuarioInfo);
            try {
                const respFavs = await fetch(`${API_URL}/favoritos/${usuario.idUsuario}`);
                const datosFavs = await respFavs.json();
                if (datosFavs.success) {
                    favoritosIds = datosFavs.data.map(fav => fav.id_producto);
                }
            } catch (e) {
                console.error("Error cargando favoritos:", e);
            }
        }

        try {
            const respuesta = await fetch(urlConFiltros);
            if (!respuesta.ok) {
                throw new Error(`Error HTTP: ${respuesta.status}`);
            }

            const datosJson = await respuesta.json();
            if (datosJson.success) {
                renderizarProductos(datosJson.data, favoritosIds);
            } else {
                mostrarError(datosJson.mensaje);
            }

        } catch (error) {
            console.error('Error al conectar con la API:', error);
            mostrarError('No se pudo conectar con el servidor. Verificá que Flask esté corriendo en el puerto 5000.');
        }
    }

    // Función para dibujar las tarjetas en el HTML
    function renderizarProductos(productos, favoritosIds = []) {
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

            // Lógica para saber si es favorito y setear los estados del botón
            const esFavorito = favoritosIds.includes(producto.id_producto);
            const btnClase = esFavorito ? 'tm-btn-primary' : 'tm-btn-ghost';
            const btnTexto = esFavorito ? '❤️ Guardado' : '❤️ Guardar';
            const estadoFav = esFavorito ? 'true' : 'false';

            const cardHTML = `
                <div class="tm-card">
                    <a href="detalle_producto.php?id=${producto.id_producto}" class="tm-card-img-link">
                        <div class="tm-card-img">
                            ${imgSrc
                                ? `<img src="${imgSrc}" alt="${producto.modelo}" 
                                        onerror="this.style.display='none'; this.parentElement.innerHTML = generarPlaceholder('${producto.marca}');">`
                                : generarPlaceholder(producto.marca)
                            }
                        </div>
                    </a>
                    <div class="tm-card-body">
                        <span class="tm-card-badge ${badgeClass}">${producto.categoria}</span>
                        <a href="detalle_producto.php?id=${producto.id_producto}" class="tm-card-title-link">
                            <h3 class="tm-card-title" title="${producto.modelo}">${producto.modelo}</h3>
                        </a>
                        <p class="tm-card-brand">${producto.marca}</p>
                        <div class="tm-card-actions">
                            <button class="tm-btn tm-btn-outline tm-btn-sm" data-id="${producto.id_producto}" data-categoria="${producto.categoria}" data-modelo="${producto.modelo}" onclick="agregarComparar(this)">
                                ⚖️ Comparar
                            </button>
                            
                            <button class="tm-btn ${btnClase} tm-btn-sm" data-id="${producto.id_producto}" data-fav="${estadoFav}" onclick="toggleFavorito(this)">
                                ${btnTexto}
                            </button>
                        </div>
                    </div>
                </div>
            `;
            contenedorProductos.insertAdjacentHTML('beforeend', cardHTML);
        });
        actualizarBotonesCatalogo();
    }

    // Clase CSS del badge según la categoría
    function obtenerBadgeClass(categoria) {
        const clases = {
            'CPU': 'tm-badge-cpu',
            'GPU': 'tm-badge-gpu',
            'RAM': 'tm-badge-ram',
            'Laptop': 'tm-badge-laptop',
            'Almacenamiento': 'tm-badge-storage'
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

// Obtener lista de comparación de sessionStorage
function obtenerComparacion() {
    const items = sessionStorage.getItem('techmatch_comparar');
    return items ? JSON.parse(items) : [];
}

// Guardar lista de comparación en sessionStorage
function guardarComparacion(items) {
    sessionStorage.setItem('techmatch_comparar', JSON.stringify(items));
    actualizarBarraComparacion();
}

// Actualizar el estado de los botones de comparar en el catálogo
function actualizarBotonesCatalogo() {
    const items = obtenerComparacion();
    const ids = items.map(item => item.id);
    
    document.querySelectorAll('[onclick="agregarComparar(this)"]').forEach(btn => {
        const id = btn.dataset.id;
        if (ids.includes(id)) {
            btn.innerHTML = '✅ Agregado';
            btn.disabled = true;
            btn.style.opacity = '0.6';
        } else {
            btn.innerHTML = '⚖️ Comparar';
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    });
}

// Agregar producto a comparación
function agregarComparar(btn) {
    const id = btn.dataset.id;
    const categoria = btn.dataset.categoria;
    const modelo = btn.dataset.modelo;
    
    let items = obtenerComparacion();
    
    // Validar categoría: todos deben ser de la misma categoría
    if (items.length > 0 && items[0].categoria !== categoria) {
        alert(`No podés comparar un producto de categoría ${categoria} con uno de categoría ${items[0].categoria}. Deben ser de la misma categoría.`);
        return;
    }
    
    // Límite máximo de 2 productos
    if (items.length >= 2) {
        alert('Solo podés comparar hasta 2 productos a la vez. Quitá uno para agregar otro.');
        return;
    }
    
    // Evitar duplicados
    if (items.some(item => item.id === id)) {
        return;
    }
    
    items.push({ id, categoria, modelo });
    guardarComparacion(items);
    actualizarBotonesCatalogo();
}

// Quitar producto de la comparación
function quitarComparar(id) {
    let items = obtenerComparacion();
    items = items.filter(item => item.id !== id);
    guardarComparacion(items);
    actualizarBotonesCatalogo();
}

// Limpiar toda la comparación
function limpiarComparar() {
    guardarComparacion([]);
    actualizarBotonesCatalogo();
}

// Redirigir a la página de comparación
function irAComparar() {
    const items = obtenerComparacion();
    if (items.length < 2) {
        alert('Seleccioná exactamente 2 productos para comparar.');
        return;
    }
    window.location.href = `comparar.php?idA=${items[0].id}&idB=${items[1].id}`;
}

// Actualizar la barra flotante de comparación
function actualizarBarraComparacion() {
    let bar = document.getElementById('compareBar');
    const items = obtenerComparacion();
    
    if (items.length === 0) {
        if (bar) {
            bar.classList.remove('visible');
            setTimeout(() => {
                const currentItems = obtenerComparacion();
                const currentBar = document.getElementById('compareBar');
                if (currentBar && currentItems.length === 0) {
                    currentBar.remove();
                }
            }, 400); // esperar a que termine la transición css
        }
        return;
    }
    
    if (!bar) {
        bar = document.createElement('div');
        bar.id = 'compareBar';
        bar.className = 'tm-compare-bar';
        document.body.appendChild(bar);
    }
    
    let itemsHTML = '';
    items.forEach(item => {
        itemsHTML += `
            <div class="tm-compare-bar-item">
                <span>${item.modelo.substring(0, 20)}${item.modelo.length > 20 ? '...' : ''}</span>
                <button class="tm-compare-bar-remove" onclick="quitarComparar('${item.id}')">×</button>
            </div>
        `;
    });
    
    bar.innerHTML = `
        <div class="tm-compare-bar-items">
            ${itemsHTML}
        </div>
        <div class="tm-compare-bar-actions">
            <button class="tm-btn tm-btn-primary tm-btn-sm" onclick="irAComparar()">⚖️ Comparar</button>
            <button class="tm-btn tm-btn-ghost tm-btn-sm" onclick="limpiarComparar()">Limpiar</button>
        </div>
    `;
    
    // Forzar reflow para animación
    bar.offsetHeight;
    bar.classList.add('visible');
}

// Inicializar la barra flotante al cargar
window.addEventListener('DOMContentLoaded', () => {
    actualizarBarraComparacion();
});

// Activar o desactivar favorito
async function toggleFavorito(btn) {
    const usuarioInfo = localStorage.getItem('techmatch_usuario');
    if (!usuarioInfo) {
        window.location.href = 'login.php?redirect=catalogo.php';
        return;
    }

    const usuario = JSON.parse(usuarioInfo);
    const idProducto = btn.dataset.id;
    const esFavorito = btn.dataset.fav === 'true'; 
    const textoOriginal = btn.innerHTML;
    
    btn.innerHTML = '⏳ Procesando...';
    btn.disabled = true;

    try {
        if (esFavorito) {
            // Ya era favorito: lo ELIMINAMOS
            const respuesta = await fetch(`${API_URL}/favoritos/eliminar`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    idUsuario: usuario.idUsuario,
                    idProducto: parseInt(idProducto)
                })
            });
            const datos = await respuesta.json();
            
            if (datos.success) {
                btn.dataset.fav = 'false';
                btn.innerHTML = '❤️ Guardar';
                btn.classList.remove('tm-btn-primary');
                btn.classList.add('tm-btn-ghost');
            } else {
                alert(datos.mensaje);
                btn.innerHTML = textoOriginal;
            }

        } else {
            // No era favorito: lo AGREGAMOS
            const respuesta = await fetch(`${API_URL}/favoritos/agregar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    idUsuario: usuario.idUsuario,
                    idProducto: parseInt(idProducto)
                })
            });
            const datos = await respuesta.json();
            
            if (datos.success) {
                btn.dataset.fav = 'true';
                btn.innerHTML = '❤️ Guardado';
                btn.classList.add('tm-btn-primary');
                btn.classList.remove('tm-btn-ghost');
            } else {
                alert(datos.mensaje);
                btn.innerHTML = textoOriginal;
            }
        }
    } catch (error) {
        console.error('Error procesando favorito:', error);
        alert('Ocurrió un error al procesar la solicitud.');
        btn.innerHTML = textoOriginal;
    } finally {
        btn.disabled = false;
    }
}
