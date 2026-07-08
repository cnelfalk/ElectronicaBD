// Detección automática del entorno para apuntar a la API Flask correcta
var API_URL;
var API_USAR_PROXY = false;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Desarrollo local en Windows: Flask corre en el servidor Linux remoto
    API_URL = 'http://100.82.23.52:5000/api';
} else if (window.location.hostname === 'proyectomans.servehttp.com') {
    // Dominio público con Caddy: el reverse_proxy de Caddy ya redirige
    // /techmatch/api/* → localhost:5000/api/* sin necesidad de proxy PHP.
    // (handle_path /techmatch/* stripea el prefijo, por eso se usa /techmatch/api)
    API_URL = '/techmatch/api';
    API_USAR_PROXY = false;
} else {
    // Acceso directo por IP de Tailscale: Caddy redirige /api/* → localhost:5000
    API_URL = '/api';
    API_USAR_PROXY = false;
}


// construirUrl - arma la URL correcta según si se usa proxy o acceso directo
function construirUrl(endpoint) {
    if (API_USAR_PROXY) {
        // El endpoint puede tener sus propios query params (ej: /productos?marca=AMD)
        // Los encodificamos en el parámetro 'ruta' del proxy
        return `${API_URL}?ruta=${encodeURIComponent(endpoint)}`;
    }
    return `${API_URL}${endpoint}`;
}

async function apiRequest(endpoint, options = {}) {
    const config = {
        headers: { 'Content-Type': 'application/json' },
        ...options
    };

    const respuesta = await fetch(construirUrl(endpoint), config);

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
