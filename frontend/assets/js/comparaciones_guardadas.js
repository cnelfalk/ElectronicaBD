document.addEventListener('DOMContentLoaded', () => {
    const contenedorComparaciones = document.getElementById('contenedorComparaciones');

    try {
        const usuarioInfo = localStorage.getItem('techmatch_usuario');

        // 1. Verificar si el usuario tiene sesión iniciada
        if (!usuarioInfo) {
            window.location.href = 'login.php?redirect=comparaciones_guardadas.php';
            return;
        }

        const usuario = JSON.parse(usuarioInfo);

        // 2. Función principal para cargar el historial
        async function cargarComparaciones() {
            const endpoint = `/comparar/historial/${usuario.idUsuario}`;

            try {
                const datosJson = await apiRequest(endpoint);

                if (datosJson.success) {
                    renderizarComparaciones(datosJson.data);
                } else {
                    mostrarError(datosJson.mensaje || 'Error al cargar las comparaciones.');
                }
            } catch (error) {
                console.error('Error al cargar comparaciones:', error);
                mostrarError('No se pudo conectar con el servidor. Revisá la consola.');
            }
        }

        // 3. Función para renderizar el listado en el DOM
        function renderizarComparaciones(historial) {
            contenedorComparaciones.innerHTML = '';

            if (historial.length === 0) {
                contenedorComparaciones.innerHTML = `
                    <div class="tm-empty" style="grid-column: 1 / -1; text-align: center; padding: 4rem 0;">
                        <div class="tm-empty-icon">⚖️</div>
                        <p style="color: var(--tm-text-secondary); font-size: 1.1rem; margin-bottom: 1.5rem;">Aún no has guardado ninguna comparación técnica.</p>
                        <a href="catalogo.php" class="tm-btn tm-btn-primary">Explorar Catálogo</a>
                    </div>
                `;
                return;
            }

            historial.forEach(comp => {
                const badgeClass = obtenerBadgeClass(comp.categoria);
                
                // Formatear fecha
                let fechaTexto = 'Desconocida';
                if (comp.fecha) {
                    const fechaObj = new Date(comp.fecha);
                    fechaTexto = fechaObj.toLocaleDateString('es-AR') + ' - ' + fechaObj.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
                }

                // Separar IDs de productos para el enlace
                const ids = comp.ids_productos ? comp.ids_productos.split(',') : [];
                const idA = ids[0] || '';
                const idB = ids[1] || '';

                const cardHTML = `
                    <div class="tm-card" id="comp-card-${comp.id_comparacion}" style="display: flex; flex-direction: column; justify-content: space-between;">
                        <div class="tm-card-body" style="padding: 1.5rem; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap; gap: 0.5rem;">
                                    <span class="tm-card-badge ${badgeClass}" style="font-size: 0.7rem; padding: 0.25rem 0.6rem;">${comp.categoria}</span>
                                    <span style="font-size: 0.75rem; color: var(--tm-text-muted);">${fechaTexto}</span>
                                </div>
                                <h3 class="tm-card-title" title="${comp.duplas_modelos}" style="font-size: 1.15rem; font-weight: 700; margin: 0 0 1rem 0; line-height: 1.4; color: var(--tm-text-primary);">
                                    ${comp.duplas_modelos}
                                </h3>
                            </div>
                            
                            <div class="tm-card-actions" style="display: flex; gap: 0.75rem; margin-top: 1.2rem;">
                                <a href="comparar.php?idA=${idA}&idB=${idB}" class="tm-btn tm-btn-primary tm-btn-sm" style="flex-grow: 1; justify-content: center; display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none; padding: 0.5rem 1rem;">
                                    ⚖️ Ver Comparación
                                </a>
                                <button class="tm-btn tm-btn-outline tm-btn-sm" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.2); padding: 0.5rem;" data-id="${comp.id_comparacion}" onclick="eliminarComparacion(this)" title="Eliminar del Historial">
                                    🗑️
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                contenedorComparaciones.insertAdjacentHTML('beforeend', cardHTML);
            });
        }

        // Ejecutar carga
        cargarComparaciones();

    } catch (errorCritico) {
        console.error("Error crítico en comparaciones_guardadas.js:", errorCritico);
        contenedorComparaciones.innerHTML = `
            <div class="tm-empty" style="grid-column: 1 / -1; color: #ef4444;">
                <div class="tm-empty-icon">⚠️</div>
                <p>Error crítico: ${errorCritico.message}</p>
            </div>
        `;
    }
});

// --- FUNCIONES GLOBALES ---
function obtenerBadgeClass(categoria) {
    const clases = { 'CPU': 'tm-badge-cpu', 'GPU': 'tm-badge-gpu', 'RAM': 'tm-badge-ram', 'Laptop': 'tm-badge-laptop', 'Almacenamiento': 'tm-badge-storage' };
    return clases[categoria] || 'tm-badge-laptop';
}

function mostrarError(mensaje) {
    const cont = document.getElementById('contenedorComparaciones');
    if (cont) {
        cont.innerHTML = `
            <div class="tm-empty" style="grid-column: 1 / -1; text-align: center; padding: 4rem 0;">
                <div class="tm-empty-icon">⚠️</div>
                <p>${mensaje}</p>
            </div>
        `;
    }
}

async function eliminarComparacion(btn) {
    const idComparacion = btn.dataset.id;
    if (!idComparacion) return;

    if (!(await mostrarConfirmacion('¿Estás seguro de que querés eliminar esta comparación de tu historial?'))) {
        return;
    }

    const iconoOriginal = btn.innerHTML;
    btn.innerHTML = '⏳';
    btn.disabled = true;

    try {
        const respuesta = await fetch(`${API_URL}/comparar/${idComparacion}`, {
            method: 'DELETE'
        });
        const datos = await respuesta.json();

        if (datos.success) {
            const tarjeta = document.getElementById(`comp-card-${idComparacion}`);
            if (tarjeta) tarjeta.remove();

            const contenedor = document.getElementById('contenedorComparaciones');
            if (contenedor.querySelectorAll('.tm-card').length === 0) {
                contenedor.innerHTML = `
                    <div class="tm-empty" style="grid-column: 1 / -1; text-align: center; padding: 4rem 0;">
                        <div class="tm-empty-icon">⚖️</div>
                        <p style="color: var(--tm-text-secondary); font-size: 1.1rem; margin-bottom: 1.5rem;">Aún no has guardado ninguna comparación técnica.</p>
                        <a href="catalogo.php" class="tm-btn tm-btn-primary">Explorar Catálogo</a>
                    </div>
                `;
            }
        } else {
            alert(datos.mensaje || 'Error al intentar eliminar la comparación.');
            btn.innerHTML = iconoOriginal;
            btn.disabled = false;
        }
    } catch (error) {
        console.error('Error al eliminar comparación:', error);
        alert('Ocurrió un error al conectar con el servidor.');
        btn.innerHTML = iconoOriginal;
        btn.disabled = false;
    }
}
