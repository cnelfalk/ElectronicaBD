console.log("🚀 [PASO 1] favoritos.js fue cargado por el navegador.");

document.addEventListener('DOMContentLoaded', () => {
    console.log("⚡ [PASO 2] El DOM cargó, iniciando lógica de favoritos...");
    const contenedorFavoritos = document.getElementById('contenedorFavoritos');

    try {
        const usuarioInfo = localStorage.getItem('techmatch_usuario');
        console.log("👤 [PASO 3] Datos en localStorage:", usuarioInfo);

        // 1. Verificar si el usuario tiene sesión iniciada
        if (!usuarioInfo) {
            console.log("❌ [PASO 4] No hay usuario logueado. Redirigiendo a login...");
            window.location.href = 'login.php?redirect=favoritos.php';
            return;
        }

        const usuario = JSON.parse(usuarioInfo);
        console.log("✅ [PASO 5] Usuario detectado:", usuario.nombreUsuario, "(ID:", usuario.idUsuario, ")");

        // 2. Función principal para buscar los favoritos
        async function cargarFavoritos() {
            const endpoint = `${API_URL}/favoritos/${usuario.idUsuario}`;
            console.log("🌐 [PASO 6] Iniciando fetch hacia:", endpoint);
            
            try {
                const respuesta = await fetch(endpoint);
                console.log("📥 [PASO 7] Respuesta recibida de Flask. Status:", respuesta.status);
                
                if (!respuesta.ok) {
                    throw new Error(`Error HTTP del servidor: ${respuesta.status}`);
                }

                const datosJson = await respuesta.json();
                console.log("📦 [PASO 8] Datos JSON parseados:", datosJson);

                if (datosJson.success) {
                    renderizarFavoritos(datosJson.data);
                } else {
                    mostrarError(datosJson.mensaje);
                }
            } catch (error) {
                console.error('❌ [ERROR EN FETCH]:', error);
                mostrarError('No se pudo conectar con el servidor. Revisá la consola (F12) para más detalles.');
            }
        }

        // 3. Función para dibujar las tarjetas en el HTML
        function renderizarFavoritos(productos) {
            contenedorFavoritos.innerHTML = '';
            console.log(`🎨 [PASO 9] Renderizando ${productos.length} productos.`);

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
                                <button class="tm-btn tm-btn-outline tm-btn-sm" data-id="${producto.id_producto}" onclick="agregarComparar(this)">
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
        // Si JS explota antes del fetch, lo mostramos en la UI para no dejar el spinner
        console.error("💥 [CRASH FATAL EN JS]:", errorCritico);
        contenedorFavoritos.innerHTML = `
            <div class="tm-empty" style="grid-column: 1 / -1; color: #ef4444;">
                <div class="tm-empty-icon">💥</div>
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

function agregarComparar(btn) {
    btn.innerHTML = '✅ Agregado';
    btn.disabled = true;
    btn.style.opacity = '0.6';
}

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