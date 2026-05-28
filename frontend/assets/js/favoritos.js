document.addEventListener('DOMContentLoaded', () => {
    const contenedorFavoritos = document.getElementById('contenedorFavoritos');

    try {
        const usuarioInfo = localStorage.getItem('techmatch_usuario');

        // 1. Verificar si el usuario tiene sesión iniciada
        if (!usuarioInfo) {
            window.location.href = 'login.php?redirect=favoritos.php';
            return;
        }

        const usuario = JSON.parse(usuarioInfo);

        // 2. Función principal para buscar los favoritos
        async function cargarFavoritos() {
            const endpoint = `${API_URL}/favoritos/${usuario.idUsuario}`;

            try {
                const respuesta = await fetch(endpoint);

                if (!respuesta.ok) {
                    throw new Error(`Error HTTP del servidor: ${respuesta.status}`);
                }

                const datosJson = await respuesta.json();

                if (datosJson.success) {
                    renderizarFavoritos(datosJson.data);
                } else {
                    mostrarError(datosJson.mensaje);
                }
            } catch (error) {
                console.error('Error al cargar favoritos:', error);
                mostrarError('No se pudo conectar con el servidor. Revisá la consola (F12) para más detalles.');
            }
        }

        // 3. Función para dibujar las tarjetas en el HTML
        function renderizarFavoritos(productos) {
            contenedorFavoritos.innerHTML = '';

            if (productos.length === 0) {
                contenedorFavoritos.innerHTML = `
                    <div class="tm-empty" style="grid-column: 1 / -1; text-align: center;">
                        <div class="tm-empty-icon">💔</div>
                        <p>Aún no has guardado ningún producto en tus favoritos.</p>
                        <a href="catalogo.php" class="tm-btn tm-btn-primary" style="margin-top: 1rem;">Explorar Catálogo</a>
                    </div>
                `;
                return;
            }

            productos.forEach(producto => {
                const imgSrc = producto.img_url || '';
                const badgeClass = obtenerBadgeClass(producto.categoria);
                
                // Validación por si la fecha viene nula desde la BD
                let fechaTexto = 'Desconocida';
                if (producto.fecha_agregado_fav) {
                    fechaTexto = new Date(producto.fecha_agregado_fav).toLocaleDateString('es-AR');
                }

                const cardHTML = `
                    <div class="tm-card" id="fav-card-${producto.id_producto}">
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
                            
                            <p style="font-size: 0.75rem; color: var(--tm-text-muted); margin-bottom: 0.8rem;">
                                Guardado el: ${fechaTexto}
                            </p>

                            <div class="tm-card-actions">
                                <button class="tm-btn tm-btn-outline tm-btn-sm" data-id="${producto.id_producto}" data-categoria="${producto.categoria}" data-modelo="${producto.modelo}" onclick="agregarComparar(this)">
                                    ⚖️ Comparar
                                </button>
                                
                                <button class="tm-btn tm-btn-primary tm-btn-sm" data-id="${producto.id_producto}" onclick="eliminarDeFavoritos(this)">
                                    ❌ Quitar
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                contenedorFavoritos.insertAdjacentHTML('beforeend', cardHTML);
            });
        }

        // Ejecutar carga
        cargarFavoritos();

    } catch (errorCritico) {
        console.error("Error crítico en favoritos.js:", errorCritico);
        contenedorFavoritos.innerHTML = `
            <div class="tm-empty" style="grid-column: 1 / -1; color: #ef4444;">
                <div class="tm-empty-icon">⚠️</div>
                <p>Error crítico en el navegador: ${errorCritico.message}</p>
                <p style="font-size: 0.8rem;">Revisá la consola presionando F12.</p>
            </div>
        `;
    }
});

// --- FUNCIONES GLOBALES ---
function obtenerBadgeClass(categoria) {
    const clases = { 'CPU': 'tm-badge-cpu', 'GPU': 'tm-badge-gpu', 'RAM': 'tm-badge-ram', 'Laptop': 'tm-badge-laptop' };
    return clases[categoria] || 'tm-badge-laptop';
}

function mostrarError(mensaje) {
    const cont = document.getElementById('contenedorFavoritos');
    if (cont) {
        cont.innerHTML = `
            <div class="tm-empty" style="grid-column: 1 / -1;">
                <div class="tm-empty-icon">⚠️</div>
                <p>${mensaje}</p>
            </div>
        `;
    }
}

function generarPlaceholder(marca) {
    const inicial = marca ? marca[0].toUpperCase() : '?';
    return `<div class="tm-card-placeholder">
                <span class="tm-card-placeholder-letter">${inicial}</span>
                <span class="tm-card-placeholder-brand">${marca || 'Sin marca'}</span>
            </div>`;
}

function obtenerComparacion() {
    const items = sessionStorage.getItem('techmatch_comparar');
    return items ? JSON.parse(items) : [];
}

function guardarComparacion(items) {
    sessionStorage.setItem('techmatch_comparar', JSON.stringify(items));
    actualizarBarraComparacion();
}

function agregarComparar(btn) {
    const id = btn.dataset.id;
    const categoria = btn.dataset.categoria;
    const modelo = btn.dataset.modelo;

    let items = obtenerComparacion();

    if (items.length > 0 && items[0].categoria !== categoria) {
        alert(`No podés comparar un producto de categoría ${categoria} con uno de categoría ${items[0].categoria}.`);
        return;
    }
    if (items.length >= 2) {
        alert('Solo podés comparar hasta 2 productos a la vez. Quitá uno para agregar otro.');
        return;
    }
    if (items.some(item => item.id === id)) {
        return;
    }

    items.push({ id, categoria, modelo });
    guardarComparacion(items);

    btn.innerHTML = '✅ Agregado';
    btn.disabled = true;
    btn.style.opacity = '0.6';
}

function quitarComparar(id) {
    let items = obtenerComparacion();
    items = items.filter(item => item.id !== id);
    guardarComparacion(items);
}

function limpiarComparar() {
    guardarComparacion([]);
}

function irAComparar() {
    const items = obtenerComparacion();
    if (items.length < 2) {
        alert('Seleccioná exactamente 2 productos para comparar.');
        return;
    }
    window.location.href = `comparar.php?idA=${items[0].id}&idB=${items[1].id}`;
}

function actualizarBarraComparacion() {
    let bar = document.getElementById('compareBar');
    const items = obtenerComparacion();

    if (items.length === 0) {
        if (bar) {
            bar.classList.remove('visible');
            setTimeout(() => {
                const currentBar = document.getElementById('compareBar');
                if (currentBar && obtenerComparacion().length === 0) currentBar.remove();
            }, 400);
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
        <div class="tm-compare-bar-items">${itemsHTML}</div>
        <div class="tm-compare-bar-actions">
            <button class="tm-btn tm-btn-primary tm-btn-sm" onclick="irAComparar()">⚖️ Comparar</button>
            <button class="tm-btn tm-btn-ghost tm-btn-sm" onclick="limpiarComparar()">Limpiar</button>
        </div>
    `;

    bar.offsetHeight;
    bar.classList.add('visible');
}

window.addEventListener('DOMContentLoaded', () => {
    actualizarBarraComparacion();
});

async function eliminarDeFavoritos(btn) {
    const usuarioInfo = localStorage.getItem('techmatch_usuario');
    if (!usuarioInfo) return;

    const usuario = JSON.parse(usuarioInfo);
    const idProducto = btn.dataset.id;
    const textoOriginal = btn.innerHTML;
    
    btn.innerHTML = '⏳ Quitándolo...';
    btn.disabled = true;

    try {
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
            const tarjeta = document.getElementById(`fav-card-${idProducto}`);
            if (tarjeta) tarjeta.remove();

            const contenedor = document.getElementById('contenedorFavoritos');
            if (contenedor.children.length === 0) {
                contenedor.innerHTML = `
                    <div class="tm-empty" style="grid-column: 1 / -1; text-align: center;">
                        <div class="tm-empty-icon">💔</div>
                        <p>Aún no has guardado ningún producto en tus favoritos.</p>
                        <a href="catalogo.php" class="tm-btn tm-btn-primary" style="margin-top: 1rem;">Explorar Catálogo</a>
                    </div>
                `;
            }
        } else {
            alert(datos.mensaje);
            btn.innerHTML = textoOriginal;
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Error eliminando favorito:', error);
        alert('Ocurrió un error al intentar quitar el producto.');
        btn.innerHTML = textoOriginal;
        btn.disabled = false;
    }
}