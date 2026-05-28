// Cplocar la IP de Tailscale o actualizar si se despliega en otro ambiente
// Se debe colocar /techmatch/api para que sea accesible públicamente
var API_URL = '/techmatch/api';

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
