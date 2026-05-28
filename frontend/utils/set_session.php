<?php
# ═══════════════════════════════════════════════════════════════════════════
# set_session.php — Endpoint para sincronizar el login de JS con la sesión PHP
# ═══════════════════════════════════════════════════════════════════════════

require_once 'session.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Leer payload JSON
    $json = file_get_contents('php://input');
    $usuario = json_decode($json, true);
    
    if ($usuario && isset($usuario['idUsuario'])) {
        login_usuario($usuario);
        echo json_encode(['success' => true, 'mensaje' => 'Sesión PHP iniciada']);
    } else {
        http_response_code(400);
        echo json_encode(['success' => false, 'mensaje' => 'Datos de usuario inválidos']);
    }
} else {
    http_response_code(405);
    echo json_encode(['success' => false, 'mensaje' => 'Método no permitido']);
}
?>
