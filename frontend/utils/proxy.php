<?php
/**
 * proxy.php — Proxy transparente hacia la API Flask de TechMatch
 * ═══════════════════════════════════════════════════════════════════
 * Resuelve el problema de las marcas y demás endpoints cuando el
 * frontend se sirve desde proyectomans.servehttp.com:
 *
 *   - El JS envía: /techmatch/api/marcas
 *   - Apache lo sirve como: /frontend/utils/proxy.php?ruta=marcas
 *   ... O mejor aún, el JS detecta el dominio y apunta aquí directamente.
 *
 * Uso directo: /frontend/utils/proxy.php?ruta=/marcas
 * O con rewrite: /techmatch/api/* → proxy.php?ruta=*
 *
 * Soporta GET, POST y DELETE.
 */

require_once __DIR__ . '/../config/api.php';

// ── Leer la ruta destino ────────────────────────────────────────────
$ruta = $_GET['ruta'] ?? '';

// Sanitizar: solo permitir rutas alfanuméricas, slashes, guiones y números
if (!preg_match('#^[a-zA-Z0-9/_\-?&=.%]+$#', $ruta)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'mensaje' => 'Ruta inválida']);
    exit;
}

$urlDestino = API_URL_PHP . '/' . ltrim($ruta, '/');

// ── Reenviar query string adicional ────────────────────────────────
$queryStr = $_SERVER['QUERY_STRING'] ?? '';
// Eliminar el parámetro 'ruta' que ya procesamos
$queryStr = preg_replace('/(^|&)ruta=[^&]*/i', '', $queryStr);
$queryStr = ltrim($queryStr, '&');

if ($queryStr) {
    $urlDestino .= (strpos($urlDestino, '?') !== false ? '&' : '?') . $queryStr;
}

// ── Configurar cURL ─────────────────────────────────────────────────
$ch = curl_init($urlDestino);
$method = $_SERVER['REQUEST_METHOD'];

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 15);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

// Propagar cabeceras relevantes
$headers = ['Content-Type: application/json'];
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

// Manejar métodos HTTP
if ($method === 'POST') {
    $body = file_get_contents('php://input');
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
} elseif ($method === 'DELETE') {
    $body = file_get_contents('php://input');
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
    if ($body) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
    }
}

// ── Ejecutar y devolver la respuesta ───────────────────────────────
$respuesta  = curl_exec($ch);
$httpStatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError  = curl_error($ch);
curl_close($ch);

if ($curlError) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'success' => false,
        'mensaje' => 'Error de conexión con el servidor de la API: ' . $curlError
    ]);
    exit;
}

// Propagar el código de estado HTTP del backend
http_response_code($httpStatus);
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
echo $respuesta;
