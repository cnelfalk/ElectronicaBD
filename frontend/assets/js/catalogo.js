document.addEventListener('DOMContentLoaded', () => {
    // Referencias a los elementos del DOM
    const contenedorProductos = document.getElementById('contenedorProductos');
    const btnAplicarFiltros   = document.getElementById('btnAplicarFiltros');
    const filtroMarca         = document.getElementById('filtroMarca');
    const filtroCategoria     = document.getElementById('filtroCategoria');
    const buscarNombre        = document.getElementById('buscarNombre');
    const filtroOrdenar       = document.getElementById('filtroOrdenar');

    // Carga las marcas desde la API y puebla el select dinámicamente
    async function cargarMarcas() {
        try {
            const resp = await fetch(`${API_URL}/marcas`);
            const data = await resp.json();
            if (data.success && data.data.length > 0) {
                data.data.forEach(marca => {
                    const opt = document.createElement('option');
                    opt.value = marca.nombreMarca;
                    opt.textContent = marca.nombreMarca;
                    filtroMarca.appendChild(opt);
                });
            }
        } catch (e) {
            console.error('Error cargando marcas:', e);
        }
    }

    // Función principal para cargar productos
    async function cargarProductos() {
        contenedorProductos.innerHTML = `
            <div class="tm-loading">
                <div class="tm-spinner"></div>
                <p>Cargando catálogo...</p>
            </div>
        `;

        // Construir la URL con los parámetros de filtro
        const params = new URLSearchParams();
        if (filtroMarca.value)     params.append('marca',     filtroMarca.value);
        if (filtroCategoria.value) params.append('categoria', filtroCategoria.value);
        if (buscarNombre.value)    params.append('busqueda',  buscarNombre.value);
        if (filtroOrdenar.value)   params.append('ordenar',   filtroOrdenar.value);

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
                                        onerror="this.style.display='none'; this.parentElement.innerHTML = generarPlaceholder('${producto.marca}', '${producto.categoria}');">`
                                : generarPlaceholder(producto.marca, producto.categoria)
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

// --- Event Listeners y Lectura de URL ---
    
    // Creamos una función asíncrona para controlar el orden de ejecución exacto
    async function inicializarCatalogo() {
        // 1. PRIMERO: Esperamos a que la API traiga todas las marcas y llene el <select>
        await cargarMarcas();

        // 2. SEGUNDO: Leemos la URL
        const parametrosURL = new URLSearchParams(window.location.search);
        
        // Aplicamos filtro de categoría si existe
        if (parametrosURL.has('categoria')) {
            const cat = parametrosURL.get('categoria');
            const catCapitalizada = cat.charAt(0).toUpperCase() + cat.slice(1);
            if (filtroCategoria.querySelector(`option[value="${catCapitalizada}"]`)) {
                filtroCategoria.value = catCapitalizada;
            } else if (filtroCategoria.querySelector(`option[value="${cat.toUpperCase()}"]`)) {
                filtroCategoria.value = cat.toUpperCase();
            }
        }

        // Aplicamos filtro de marca si existe (ahora sí las opciones ya existen en el HTML)
        if (parametrosURL.has('marca')) {
            const marcaUrl = parametrosURL.get('marca');
            const option = Array.from(filtroMarca.options).find(opt => opt.value.toLowerCase() === marcaUrl.toLowerCase());
            if (option) {
                filtroMarca.value = option.value;
            }
        }

        // 3. TERCERO: Con los selects ya configurados correctamente, pedimos los productos
        cargarProductos();
    }

    // Arrancamos el proceso
    inicializarCatalogo();

    // Asignamos los eventos a los botones
    btnAplicarFiltros.addEventListener('click', cargarProductos);
    buscarNombre.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') cargarProductos();
    });
});

// generarPlaceholder - Genera un placeholder visual con ícono SVG según la categoría del producto
function generarPlaceholder(marca, categoria) {
    const iconosSVG = {
        'CPU': `<svg viewBox="0 0 64 64" width="64" height="64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="16" y="16" width="32" height="32" rx="4" stroke="#6c5ce7" stroke-width="2" fill="#6c5ce720"/>
            <rect x="24" y="24" width="16" height="16" rx="2" fill="#6c5ce7" opacity="0.6"/>
            <line x1="20" y1="12" x2="20" y2="16" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="28" y1="12" x2="28" y2="16" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="36" y1="12" x2="36" y2="16" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="44" y1="12" x2="44" y2="16" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="20" y1="48" x2="20" y2="52" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="28" y1="48" x2="28" y2="52" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="36" y1="48" x2="36" y2="52" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="44" y1="48" x2="44" y2="52" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="12" y1="20" x2="16" y2="20" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="12" y1="28" x2="16" y2="28" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="12" y1="36" x2="16" y2="36" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="12" y1="44" x2="16" y2="44" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="48" y1="20" x2="52" y2="20" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="48" y1="28" x2="52" y2="28" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="48" y1="36" x2="52" y2="36" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
            <line x1="48" y1="44" x2="52" y2="44" stroke="#6c5ce7" stroke-width="2" stroke-linecap="round"/>
        </svg>`,
        'GPU': `<svg viewBox="0 0 64 64" width="64" height="64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="6" y="18" width="52" height="28" rx="4" stroke="#00b894" stroke-width="2" fill="#00b89420"/>
            <circle cx="20" cy="32" r="8" stroke="#00b894" stroke-width="2" fill="#00b89430"/>
            <circle cx="44" cy="32" r="6" stroke="#00b894" stroke-width="2" fill="#00b89430"/>
            <line x1="14" y1="46" x2="14" y2="52" stroke="#00b894" stroke-width="2" stroke-linecap="round"/>
            <line x1="22" y1="46" x2="22" y2="52" stroke="#00b894" stroke-width="2" stroke-linecap="round"/>
            <line x1="30" y1="46" x2="30" y2="52" stroke="#00b894" stroke-width="2" stroke-linecap="round"/>
            <rect x="6" y="14" width="4" height="8" rx="1" fill="#00b894" opacity="0.5"/>
        </svg>`,
        'RAM': `<svg viewBox="0 0 64 64" width="64" height="64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="20" width="56" height="24" rx="3" stroke="#fdcb6e" stroke-width="2" fill="#fdcb6e20"/>
            <rect x="10" y="25" width="6" height="14" rx="1" fill="#fdcb6e" opacity="0.5"/>
            <rect x="19" y="25" width="6" height="14" rx="1" fill="#fdcb6e" opacity="0.5"/>
            <rect x="28" y="25" width="6" height="14" rx="1" fill="#fdcb6e" opacity="0.5"/>
            <rect x="37" y="25" width="6" height="14" rx="1" fill="#fdcb6e" opacity="0.5"/>
            <rect x="46" y="25" width="6" height="14" rx="1" fill="#fdcb6e" opacity="0.5"/>
            <rect x="24" y="44" width="16" height="4" rx="1" fill="#fdcb6e" opacity="0.3"/>
        </svg>`,
        'Laptop': `<svg viewBox="0 0 64 64" width="64" height="64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="10" y="12" width="44" height="30" rx="3" stroke="#74b9ff" stroke-width="2" fill="#74b9ff20"/>
            <rect x="14" y="16" width="36" height="22" rx="1" fill="#74b9ff" opacity="0.15"/>
            <path d="M4 46 Q4 42 10 42 L54 42 Q60 42 60 46 L60 48 Q60 50 58 50 L6 50 Q4 50 4 48 Z" stroke="#74b9ff" stroke-width="2" fill="#74b9ff20"/>
        </svg>`,
        'Almacenamiento': `<svg viewBox="0 0 64 64" width="64" height="64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="12" y="12" width="40" height="40" rx="4" stroke="#a29bfe" stroke-width="2" fill="#a29bfe20"/>
            <circle cx="32" cy="28" r="10" stroke="#a29bfe" stroke-width="2" fill="#a29bfe15"/>
            <circle cx="32" cy="28" r="3" fill="#a29bfe" opacity="0.6"/>
            <rect x="18" y="42" width="28" height="4" rx="2" fill="#a29bfe" opacity="0.4"/>
        </svg>`
    };
    const icono = iconosSVG[categoria] || iconosSVG['Laptop'];
    return `<div class="tm-card-placeholder">
                ${icono}
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
        // Usamos tu función personalizada con 'await' para que pause el código
        const irALogin = await mostrarConfirmacion("Debes registrarte para guardar productos en favoritos. ¿Querés iniciar sesión ahora?");
        
        // Solo redirige si el usuario le da a "Aceptar/Sí"
        if (irALogin) {
            window.location.href = 'login.php?redirect=catalogo.php';
        }
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