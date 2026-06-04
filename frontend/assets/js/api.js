// Colocar la IP de Tailscale o actualizar si se despliega en otro ambiente
// Se detecta automáticamente si se está probando en localhost o 127.0.0.1
var API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:5000/api'
    : 'http://100.82.23.52:5000/api';

async function apiRequest(endpoint, options = {}) {
    const config = {
        headers: { 'Content-Type': 'application/json' },
        ...options
    };

    const respuesta = await fetch(`${API_URL}${endpoint}`, config);

    if (!respuesta.ok) {
        let msg = `Error HTTP: ${respuesta.status}`;
        try {
            const data = await respuesta.json();
            if (data && data.mensaje) {
                msg = data.mensaje;
            }
        } catch (e) {
            // No es JSON, usar el fallback
        }
        throw new Error(msg);
    }

    return respuesta.json();
}
