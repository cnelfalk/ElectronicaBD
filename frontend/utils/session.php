<?php
# ═══════════════════════════════════════════════════════════════════════════
# session.php — Gestión y Seguridad de Sesiones PHP en TechMatch
# ═══════════════════════════════════════════════════════════════════════════

/**
 * Inicia la sesión de PHP de forma segura aplicando directivas de seguridad.
 * Previene el secuestro de sesión (Session Hijacking) y ataques de fijación.
 */
function session_start_safe() {
    if (session_status() === PHP_SESSION_NONE) {
        // Directivas de seguridad para cookies de sesión
        ini_set('session.use_only_cookies', 1);
        ini_set('session.use_trans_sid', 0);
        
        // Configurar parámetros de la cookie de sesión
        $cookieParams = [
            'lifetime' => 0, // Expira al cerrar el navegador
            'path' => '/',
            'domain' => '',
            'secure' => isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on', // Solo HTTPS si está disponible
            'httponly' => true, // Previene acceso de scripts JS a la cookie de sesión
            'samesite' => 'Lax' // Previene envío de cookies en navegaciones externas sospechosas
        ];
        
        session_set_cookie_params($cookieParams);
        session_start();
    }
}

/**
 * Registra los datos del usuario en la sesión al iniciar sesión exitosamente.
 *
 * @param array $usuario Datos del usuario provistos por la API.
 */
function login_usuario($usuario) {
    session_start_safe();
    
    // Regenerar ID de sesión para prevenir Session Fixation en el login
    session_regenerate_id(true);
    
    $_SESSION['usuario'] = [
        'idUsuario' => $usuario['idUsuario'] ?? null,
        'nombreUsuario' => $usuario['nombreUsuario'] ?? null,
        'emailUsuario' => $usuario['emailUsuario'] ?? null
    ];
}

/**
 * Destruye la sesión del usuario actual y elimina su cookie de sesión.
 */
function logout_usuario() {
    session_start_safe();
    
    // Vaciar array de sesión
    $_SESSION = [];
    
    // Borrar la cookie de sesión del navegador
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(
            session_name(),
            '',
            time() - 42000,
            $params["path"],
            $params["domain"],
            $params["secure"],
            $params["httponly"]
        );
    }
    
    // Destruir la sesión en servidor
    session_destroy();
}

/**
 * Retorna la información del usuario logueado en la sesión actual.
 *
 * @return array|null Datos del usuario o null si no está autenticado.
 */
function obtener_usuario_actual() {
    session_start_safe();
    return $_SESSION['usuario'] ?? null;
}

/**
 * Comprueba si el usuario actual está autenticado.
 *
 * @return bool True si está autenticado, False en caso contrario.
 */
function usuario_autenticado() {
    return obtener_usuario_actual() !== null;
}

/**
 * Requiere que el usuario esté logueado. En caso de no estarlo,
 * lo redirige a la página de login y pasa la página actual como redirect.
 */
function requerir_autenticacion() {
    if (!usuario_autenticado()) {
        $redir = basename($_SERVER['PHP_SELF']);
        $query = $_SERVER['QUERY_STRING'] ?? '';
        if ($query) {
            $redir .= '?' . $query;
        }
        
        $login_url = 'login.php?redirect=' . urlencode($redir);
        header("Location: $login_url");
        exit;
    }
}
?>
