<?php
# ═══════════════════════════════════════════════════════════════════════════
# api.php — Configuración de la API para el Frontend de TechMatch
# ═══════════════════════════════════════════════════════════════════════════

// IP del servidor Linux Mint que aloja la API Flask (red local o Tailscale)
define('API_HOST', '100.82.23.52');
define('API_PORT', '5000');

// URL Base de la API REST para su uso en PHP (cURL server-side)
define('API_URL_PHP', 'http://' . API_HOST . ':' . API_PORT . '/api');
?>
