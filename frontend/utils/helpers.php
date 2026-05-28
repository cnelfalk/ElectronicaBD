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

/**
 * Realiza una petición HTTP (cURL) del lado del servidor hacia el Backend de Flask.
 * Permite a PHP interactuar directamente con la API sin depender de JS.
 *
 * @param string $endpoint Endpoint de la API (ej: '/productos/1').
 * @param string $method Método HTTP (GET, POST, DELETE, etc.).
 * @param array|null $data Datos a enviar (para POST/PUT).
 * @return array|null Respuesta JSON decodificada como array asociativo.
 */
function consumir_api($endpoint, $method = 'GET', $data = null) {
    $url = obtener_url_api() . '/' . ltrim($endpoint, '/');
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    
    $headers = [
        'Accept: application/json'
    ];

    if ($data !== null) {
        $payload = json_encode($data);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        $headers[] = 'Content-Type: application/json';
        $headers[] = 'Content-Length: ' . strlen($payload);
    }
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($response === false || $http_code >= 400) {
        return null;
    }
    
    return json_decode($response, true);
}

/**
 * Redirecciona de forma segura a una URL y termina la ejecución.
 *
 * @param string $url URL de destino.
 */
function redireccionar($url) {
    header("Location: $url");
    exit;
}
?>
