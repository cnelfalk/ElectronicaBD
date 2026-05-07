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
            <div class="col-12 text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
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
            // Realizar la petición HTTP al backend Flask
            const respuesta = await fetch(urlConFiltros);

            // Si la respuesta no es OK (ej. 500 error del servidor)
            if (!respuesta.ok) {
                throw new Error(`Error HTTP: ${respuesta.status}`);
            }

            const datosJson = await respuesta.json();

            // Si el backend responde que fue exitoso
            if (datosJson.success) {
                renderizarProductos(datosJson.data);
            } else {
                mostrarError(datosJson.mensaje);
            }

        } catch (error) {
            console.error('Error al conectar con la API:', error);
            mostrarError('No se pudo conectar con el servidor. Verificá que Flask esté corriendo.');
        }
    }

    // Función para dibujar las tarjetas (cards) en el HTML
    function renderizarProductos(productos) {
        contenedorProductos.innerHTML = ''; // Limpiar contenedor

        if (productos.length === 0) {
            contenedorProductos.innerHTML = '<div class="col-12 text-center"><p>No se encontraron productos con esos filtros.</p></div>';
            return;
        }

        productos.forEach(producto => {
            const imgSrc = producto.img_url || '';
            // Crear el HTML de la tarjeta para cada producto
            const cardHTML = `
                <div class="col-md-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        ${imgSrc
                            ? `<img src="${imgSrc}" class="card-img-top p-3" alt="${producto.modelo}" style="object-fit: contain; height: 150px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                               <div class="card-img-placeholder" style="display:none; height:150px;">${obtenerImagenSVG(producto.marca)}</div>`
                            : `<div class="card-img-placeholder" style="height:150px;">${obtenerImagenSVG(producto.marca)}</div>`
                        }
                        <div class="card-body d-flex flex-column">
                            <span class="badge bg-secondary mb-2 align-self-start">${producto.categoria}</span>
                            <h5 class="card-title text-truncate" title="${producto.modelo}">${producto.modelo}</h5>
                            <p class="card-text text-muted small">${producto.marca}</p>
                            
                            <!-- Botones de acción -->
                            <div class="mt-auto d-grid gap-2">
                                <button class="btn btn-outline-primary btn-sm btn-comparar" data-id="${producto.id_producto}">
                                    Añadir a Comparar
                                </button>
                                <button class="btn btn-light btn-sm btn-favorito" data-id="${producto.id_producto}" onclick="guardarFavorito(this)">
                                    ❤️ Guardar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            // Insertar el HTML en el contenedor
            contenedorProductos.insertAdjacentHTML('beforeend', cardHTML);
        });
    }

    // Función para mostrar mensajes de error amigables
    function mostrarError(mensaje) {
        contenedorProductos.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger" role="alert">
                    ${mensaje}
                </div>
            </div>
        `;
    }

    // --- Event Listeners ---

    // Cargar productos al iniciar la página
    cargarProductos();

    // Recargar productos cuando el usuario hace clic en "Aplicar Filtros"
    btnAplicarFiltros.addEventListener('click', cargarProductos);

    // Opcional: Recargar al presionar "Enter" en el buscador
    buscarNombre.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') cargarProductos();
    });
});

function obtenerImagenSVG(marca) {
    const colores = {
        'Asus':   { bg: '#00539b', texto: '#ffffff' },
        'Lenovo': { bg: '#e2231a', texto: '#ffffff' },
        'Intel':  { bg: '#0071c5', texto: '#ffffff' },
        'AMD':    { bg: '#ed1c24', texto: '#ffffff' },
        'MSI':    { bg: '#d00000', texto: '#ffffff' },
        'HP':     { bg: '#0096d6', texto: '#ffffff' },
        'Dell':   { bg: '#007db8', texto: '#ffffff' },
    };
    const c = colores[marca] || { bg: '#6c757d', texto: '#ffffff' };
    const inicial = marca ? marca[0].toUpperCase() : '?';
    return `<div style="width:100%; height:100%; background:${c.bg}; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:8px 8px 0 0;">
                <span style="color:${c.texto}; font-size:2.5rem; font-weight:700; font-family:sans-serif;">${inicial}</span>
                <span style="color:${c.texto}; font-size:0.75rem; font-family:sans-serif; opacity:0.85;">${marca}</span>
            </div>`;
}

function guardarFavorito(btn) {
    const usuario = localStorage.getItem('techmatch_usuario');

    if (!usuario) {
        window.location.href = 'login.php?redirect=catalogo.php';
        return;
    }

    // TODO: conectar con el endpoint de favoritos (Prioridad 3)
    btn.textContent = '✅ Guardado';
    btn.disabled = true;
}