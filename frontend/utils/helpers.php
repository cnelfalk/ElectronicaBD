<?php
# ═══════════════════════════════════════════════════════════════════════════
# helpers.php — Funciones de utilidad generales para el Frontend de TechMatch
# ═══════════════════════════════════════════════════════════════════════════

/**
 * Sanitiza una cadena de texto para prevenir ataques XSS (Cross-Site Scripting).
 * Se debe usar siempre al renderizar datos dinámicos en HTML.
 *
 * @param string|null $data Texto a sanitizar.
 * @return string Texto sanitizado seguro para HTML.
 */
function sanitize($data) {
    if ($data === null) {
        return '';
    }
    return htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
}

/**
 * Formatea un monto numérico a formato de pesos argentinos ($.###,##).
 *
 * @param mixed $monto Monto a formatear.
 * @return string Monto formateado con signo de pesos.
 */
function format_precio($monto) {
    $num = floatval($monto);
    return '$ ' . number_format($num, 2, ',', '.');
}

require_once dirname(__DIR__) . '/config/api.php';

/**
 * Retorna la URL base del Backend (API REST de Flask).
 * Lee de la configuración centralizada.
 *
 * @return string URL base de la API.
 */
function obtener_url_api() {
    return API_URL_PHP;
}

?>

