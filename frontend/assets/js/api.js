// IP de Tailscale — actualizar si se despliega en otro ambiente
var API_URL = 'http://100.82.23.52:5000/api';

async function apiRequest(endpoint, options = {}) {
    const config = {
        headers: { 'Content-Type': 'application/json' },
        ...options
    };

    const respuesta = await fetch(`${API_URL}${endpoint}`, config);

    if (!respuesta.ok) {
        throw new Error(`Error HTTP: ${respuesta.status}`);
    }

    return respuesta.json();
}
