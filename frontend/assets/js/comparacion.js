document.addEventListener('DOMContentLoaded', () => {
    // 1. Extraer los parámetros de la URL
    const params = new URLSearchParams(window.location.search);
    let idA = params.get('idA');
    let idB = params.get('idB');

    // Referencias del DOM
    const compareCargando = document.getElementById('comparacionCargando');
    const compareError = document.getElementById('comparacionError');
    const compareContenido = document.getElementById('comparacionContenido');
    const errorMensaje = document.getElementById('errorMensaje');
    const selectPerfilUso = document.getElementById('perfilUso');
    const btnGuardarComparacion = document.getElementById('btnGuardarComparacion');

    // Obtener información del usuario logueado
    const usuarioInfo = localStorage.getItem('techmatch_usuario');
    let usuario = null;
    if (usuarioInfo) {
        usuario = JSON.parse(usuarioInfo);
    }

    const ganadorNombre = document.getElementById('ganadorNombre');
    const ganadorMotivo = document.getElementById('ganadorMotivo');
    const nombreProductoA = document.getElementById('nombreProductoA');
    const nombreProductoB = document.getElementById('nombreProductoB');
    const precioTituloA = document.getElementById('precioTituloA');
    const precioTituloB = document.getElementById('precioTituloB');
    const tablaEspecificaciones = document.getElementById('tablaEspecificaciones');
    const preciosListaA = document.getElementById('preciosListaA');
    const preciosListaB = document.getElementById('preciosListaB');

    // Validar parámetros mínimos
    if (!idA || !idB) {
        // Fallback al sessionStorage si por algún motivo no vienen en la URL
        const items = sessionStorage.getItem('techmatch_comparar');
        if (items) {
            const parsed = JSON.parse(items);
            if (parsed.length >= 2) {
                idA = parsed[0].id;
                idB = parsed[1].id;
            }
        }
    }

    if (!idA || !idB) {
        mostrarError('Se requieren exactamente dos productos seleccionados para comparar.');
        return;
    }

    // Escuchar cambios en el selector de Perfil de Uso
    selectPerfilUso.addEventListener('change', () => {
        cargarComparacion(selectPerfilUso.value);
    });

    // Escuchar el botón de Guardar Comparación
    if (btnGuardarComparacion) {
        btnGuardarComparacion.addEventListener('click', async () => {
            if (!usuario) return;
            
            btnGuardarComparacion.innerHTML = '⏳ Guardando...';
            btnGuardarComparacion.disabled = true;

            try {
                const respuesta = await fetch(`${API_URL}/comparar/guardar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        idUsuario: usuario.idUsuario,
                        idProductoA: parseInt(idA),
                        idProductoB: parseInt(idB)
                    })
                });

                const datosJson = await respuesta.json();
                if (datosJson.success) {
                    btnGuardarComparacion.innerHTML = '✅ Guardada en Mis Comparaciones';
                    btnGuardarComparacion.style.opacity = '0.7';
                } else {
                    alert(datosJson.mensaje || 'Error al guardar la comparación.');
                    btnGuardarComparacion.innerHTML = '💾 Guardar Comparación';
                    btnGuardarComparacion.disabled = false;
                }
            } catch (error) {
                console.error('Error al guardar comparación:', error);
                alert('No se pudo guardar la comparación. Verificá tu conexión.');
                btnGuardarComparacion.innerHTML = '💾 Guardar Comparación';
                btnGuardarComparacion.disabled = false;
            }
        });
    }

    // Cargar comparación inicial
    cargarComparacion(selectPerfilUso.value);

    // Función para obtener la recomendación de la API
    async function cargarComparacion(perfil) {
        mostrarCargando();

        try {
            const datos = await apiRequest(`/comparar?idA=${idA}&idB=${idB}&perfil=${encodeURIComponent(perfil)}`);
            if (datos.success) {
                renderizarComparacion(datos);
            } else {
                mostrarError(datos.mensaje || 'Error al obtener la recomendación.');
            }
        } catch (error) {
            console.error('Error al conectar con la API de comparación:', error);
            mostrarError('No se pudo conectar con el servidor. Verificá que el backend esté corriendo.');
        }
    }

    // Funciones de control de estado visual
    function mostrarCargando() {
        compareCargando.style.display = 'flex';
        compareError.style.display = 'none';
        compareContenido.style.display = 'none';
    }

    function mostrarError(mensaje) {
        compareCargando.style.display = 'none';
        compareError.style.display = 'block';
        compareContenido.style.display = 'none';
        errorMensaje.textContent = mensaje;
    }

    function renderizarComparacion(data) {
        compareCargando.style.display = 'none';
        compareError.style.display = 'none';
        compareContenido.style.display = 'block';

        // 1. Ganador / Recomendación
        ganadorNombre.textContent = data.ganador;
        ganadorMotivo.textContent = data.motivo;

        // Mostrar botón de guardar si el usuario está logueado
        if (usuario && btnGuardarComparacion) {
            btnGuardarComparacion.style.display = 'inline-flex';
            btnGuardarComparacion.disabled = false;
            btnGuardarComparacion.innerHTML = '💾 Guardar Comparación';
            btnGuardarComparacion.style.opacity = '1';
        }

        // 2. Cabeceras de tabla y títulos
        nombreProductoA.textContent = data.datosA.modelo;
        nombreProductoB.textContent = data.datosB.modelo;
        precioTituloA.textContent = `Precios de ${data.datosA.modelo}`;
        precioTituloB.textContent = `Precios de ${data.datosB.modelo}`;

        // 3. Renderizar especificaciones side-by-side
        tablaEspecificaciones.innerHTML = '';
        const categoria = data.categoria;

        let specs = [];
        if (categoria === 'Laptop') {
            specs = [
                { label: 'Procesador (CPU)',    valA: data.datosA.cpu_modelo,   valB: data.datosB.cpu_modelo,   rawA: data.datosA.cpu_score,         rawB: data.datosB.cpu_score,         highlight: true },
                { label: 'Placa de Video (GPU)',valA: data.datosA.gpu_modelo,   valB: data.datosB.gpu_modelo,   highlight: false },
                { label: 'Memoria RAM',         valA: `${data.datosA.ram_gb} GB`,           valB: `${data.datosB.ram_gb} GB`,           rawA: data.datosA.ram_gb,            rawB: data.datosB.ram_gb,            highlight: true },
                { label: 'Almacenamiento',      valA: `${data.datosA.almacenamiento_gb} GB`, valB: `${data.datosB.almacenamiento_gb} GB`, rawA: data.datosA.almacenamiento_gb, rawB: data.datosB.almacenamiento_gb, highlight: true },
                { label: 'Pantalla',            valA: `${data.datosA.tamanio_pantalla}" (${data.datosA.tasa_refresco_hz}Hz)`, valB: `${data.datosB.tamanio_pantalla}" (${data.datosB.tasa_refresco_hz}Hz)`, rawA: data.datosA.tasa_refresco_hz, rawB: data.datosB.tasa_refresco_hz, highlight: true },
                { label: 'Capacidad de Batería',valA: `${data.datosA.capacidad_bateria_wh} Wh`, valB: `${data.datosB.capacidad_bateria_wh} Wh`, rawA: data.datosA.capacidad_bateria_wh, rawB: data.datosB.capacidad_bateria_wh, highlight: true },
                { label: 'Peso',                valA: `${data.datosA.peso_kg} kg`, valB: `${data.datosB.peso_kg} kg`, rawA: data.datosA.peso_kg, rawB: data.datosB.peso_kg, highlight: true, menorEsMejor: true }
            ];
        } else if (categoria === 'CPU') {
            specs = [
                { label: 'Núcleos',             valA: data.datosA.nucleos,         valB: data.datosB.nucleos,         rawA: data.datosA.nucleos,         rawB: data.datosB.nucleos,         highlight: true },
                { label: 'Hilos',               valA: data.datosA.hilos,           valB: data.datosB.hilos,           rawA: data.datosA.hilos,           rawB: data.datosB.hilos,           highlight: true },
                { label: 'Frecuencia Base',     valA: `${data.datosA.frecuencia_base} GHz`,  valB: `${data.datosB.frecuencia_base} GHz`,  rawA: data.datosA.frecuencia_base,  rawB: data.datosB.frecuencia_base,  highlight: true },
                { label: 'Frecuencia Turbo',    valA: `${data.datosA.frecuencia_turbo} GHz`, valB: `${data.datosB.frecuencia_turbo} GHz`, rawA: data.datosA.frecuencia_turbo, rawB: data.datosB.frecuencia_turbo, highlight: true },
                { label: 'TDP (Consumo/Calor)', valA: `${data.datosA.tdp} W`,      valB: `${data.datosB.tdp} W`,      rawA: data.datosA.tdp,             rawB: data.datosB.tdp,             highlight: true, menorEsMejor: true }
            ];
        } else if (categoria === 'GPU') {
            specs = [
                { label: 'VRAM',            valA: `${data.datosA.vram_gb} GB`,  valB: `${data.datosB.vram_gb} GB`,  rawA: data.datosA.vram_gb,    rawB: data.datosB.vram_gb,    highlight: true },
                { label: 'Tipo de Memoria', valA: data.datosA.tipo_memoria,     valB: data.datosB.tipo_memoria,     highlight: false },
                { label: 'Bus de Memoria',  valA: data.datosA.bus_bits ? `${data.datosA.bus_bits} bits` : '-', valB: data.datosB.bus_bits ? `${data.datosB.bus_bits} bits` : '-', rawA: data.datosA.bus_bits, rawB: data.datosB.bus_bits, highlight: true },
                { label: 'TDP',             valA: `${data.datosA.tdp_w} W`,     valB: `${data.datosB.tdp_w} W`,     rawA: data.datosA.tdp_w,      rawB: data.datosB.tdp_w,      highlight: true, menorEsMejor: true }
            ];
        } else if (categoria === 'RAM') {
            specs = [
                { label: 'Capacidad',     valA: `${data.datosA.capacidad_gb} GB`,    valB: `${data.datosB.capacidad_gb} GB`,    rawA: data.datosA.capacidad_gb,  rawB: data.datosB.capacidad_gb,  highlight: true },
                { label: 'Tipo',          valA: data.datosA.tipo_memoria,             valB: data.datosB.tipo_memoria,             highlight: false },
                { label: 'Velocidad',     valA: `${data.datosA.velocidad_mhz} MHz`,   valB: `${data.datosB.velocidad_mhz} MHz`,   rawA: data.datosA.velocidad_mhz, rawB: data.datosB.velocidad_mhz, highlight: true },
                { label: 'Módulos',       valA: data.datosA.cantidad_modulos || '-',  valB: data.datosB.cantidad_modulos || '-',  highlight: false },
                { label: 'Latencia CAS',  valA: data.datosA.latencia ? `CL${data.datosA.latencia}` : '-', valB: data.datosB.latencia ? `CL${data.datosB.latencia}` : '-', rawA: data.datosA.latencia, rawB: data.datosB.latencia, highlight: true, menorEsMejor: true }
            ];
        } else if (categoria === 'Almacenamiento') {
            specs = [
                { label: 'Capacidad',         valA: `${data.datosA.capacidad_gb} GB`,       valB: `${data.datosB.capacidad_gb} GB`,       rawA: data.datosA.capacidad_gb,      rawB: data.datosB.capacidad_gb,      highlight: true },
                { label: 'Tipo',              valA: data.datosA.tipo_disco,                  valB: data.datosB.tipo_disco,                  highlight: false },
                { label: 'Interfaz',          valA: data.datosA.interfaz || '-',             valB: data.datosB.interfaz || '-',             highlight: false },
                { label: 'Velocidad Lectura', valA: `${data.datosA.velocidad_lectura} MB/s`, valB: `${data.datosB.velocidad_lectura} MB/s`, rawA: data.datosA.velocidad_lectura, rawB: data.datosB.velocidad_lectura, highlight: true }
            ];
        }

        specs.forEach(spec => {
            let classes = { classA: '', classB: '' };
            if (spec.highlight) {
                classes = compararValores(
                    spec.rawA !== undefined ? spec.rawA : spec.valA,
                    spec.rawB !== undefined ? spec.rawB : spec.valB,
                    spec.menorEsMejor
                );
            }

            const rowHTML = `
                <tr>
                    <td class="tm-compare-feature-name">${spec.label}</td>
                    <td class="tm-compare-col-a ${classes.classA}">${spec.valA}</td>
                    <td class="tm-compare-col-b ${classes.classB}">${spec.valB}</td>
                </tr>
            `;
            tablaEspecificaciones.insertAdjacentHTML('beforeend', rowHTML);
        });

        // 4. Renderizar tiendas y precios
        renderPrecios(data.preciosA, preciosListaA);
        renderPrecios(data.preciosB, preciosListaB);
    }

    // Helper para comparar valores y resaltar
    function compararValores(valA, valB, menorEsMejor = false) {
        const numA = parseFloat(valA);
        const numB = parseFloat(valB);

        if (isNaN(numA) || isNaN(numB)) {
            return { classA: '', classB: '' };
        }

        if (numA === numB) {
            return { classA: '', classB: '' };
        }

        const esMejorA = menorEsMejor ? (numA < numB) : (numA > numB);
        return {
            classA: esMejorA ? 'tm-highlight-winner' : '',
            classB: !esMejorA ? 'tm-highlight-winner' : ''
        };
    }

    // Helper para dibujar lista de precios
    function renderPrecios(precios, contenedor) {
        contenedor.innerHTML = '';
        if (!precios || precios.length === 0) {
            contenedor.innerHTML = `
                <div style="color: var(--tm-text-muted); font-size: 0.9rem; text-align: center; padding: 1rem 0;">
                    No hay precios disponibles en este momento.
                </div>
            `;
            return;
        }

        precios.forEach(p => {
            const rowHTML = `
                <div class="tm-price-row">
                    <div style="display: flex; flex-direction: column;">
                        <span class="tm-store-name">${p.nombre_tienda}</span>
                        <span style="font-size: 0.7rem; color: var(--tm-text-muted);">Act: ${new Date(p.fec_actualizacion).toLocaleDateString('es-AR')}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span class="tm-store-price">$${parseFloat(p.precio).toLocaleString('es-AR', {minimumFractionDigits: 0, maximumFractionDigits: 0})}</span>
                        <a href="${p.url_producto}" target="_blank" class="tm-btn tm-btn-primary tm-btn-sm tm-store-link">Ver Oferta</a>
                    </div>
                </div>
            `;
            contenedor.insertAdjacentHTML('beforeend', rowHTML);
        });
    }
});
