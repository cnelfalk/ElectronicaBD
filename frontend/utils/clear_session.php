<?php
# ═══════════════════════════════════════════════════════════════════════════
# clear_session.php — Endpoint para sincronizar el logout de JS con la sesión PHP
# ═══════════════════════════════════════════════════════════════════════════

require_once 'session.php';

header('Content-Type: application/json');

logout_usuario();
echo json_encode(['success' => true, 'mensaje' => 'Sesión PHP destruida']);
?>
