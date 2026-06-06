<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Iniciar Sesión</title>
    <meta name="description" content="Iniciá sesión en TechMatch para guardar favoritos y comparaciones.">
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <div class="tm-auth-wrapper">
        <div class="tm-auth-card">
            <h2>Bienvenido de vuelta</h2>
            <p class="tm-subtitle">Ingresá a tu cuenta de TechMatch</p>

            <div id="alerta-error" class="tm-alert tm-alert-error"></div>

            <form id="form-login">
                <div class="tm-form-group">
                    <label for="identificador">Correo electrónico o Usuario</label>
                    <input type="text" class="tm-input" id="identificador" placeholder="tu@email.com o nombre de usuario" required>
                </div>
                <div class="tm-form-group">
                    <label for="contrasenia">Contraseña</label>
                    <div class="tm-password-wrapper">
                        <input type="password" class="tm-input" id="contrasenia" placeholder="Tu contraseña" required>
                        <button type="button" class="tm-password-toggle" onclick="togglePasswordVisibility('contrasenia', this)" aria-label="Mostrar/ocultar contraseña">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                                <line class="eye-slash" x1="3" y1="3" x2="21" y2="21"></line>
                            </svg>
                        </button>
                    </div>
                </div>
                <button type="submit" class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg" id="btn-submit">
                    Ingresar
                </button>
            </form>

            <p style="text-align: center; margin-top: 1rem;">
                <a href="recuperar.php" style="font-size: 0.85rem; color: var(--tm-text-muted); transition: color 0.2s;"
                   onmouseover="this.style.color='var(--tm-accent)'" onmouseout="this.style.color='var(--tm-text-muted)'">
                    ¿Olvidaste tu contraseña?
                </a>
            </p>

            <hr class="tm-divider">
            <p class="tm-auth-footer">
                ¿No tenés cuenta? <a href="registro.php">Registrate acá</a>
            </p>
        </div>
    </div>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script>
        // Si ya está logueado, redirigir al catálogo
        if (localStorage.getItem('techmatch_usuario')) {
            window.location.href = 'catalogo.php';
        }

        document.getElementById('form-login').addEventListener('submit', async function (e) {
            e.preventDefault();

            const btnSubmit = document.getElementById('btn-submit');
            const alertaError = document.getElementById('alerta-error');

            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Ingresando...';
            alertaError.classList.remove('visible');

            // CAMBIO: Capturamos el nuevo ID 'identificador'
            const identificador = document.getElementById('identificador').value.trim();
            const contrasenia = document.getElementById('contrasenia').value;

            try {
                const respuesta = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        // CAMBIO: Enviamos la propiedad 'identificador' al backend en lugar de 'emailUsuario'
                        identificador: identificador,
                        contraseniaUsuario: contrasenia
                    })
                });

                const datos = await respuesta.json();

                if (datos.success) {
                    localStorage.setItem('techmatch_usuario', JSON.stringify(datos.datos));
                    // Sincronizar con la sesión de PHP
                    await fetch('utils/set_session.php', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(datos.datos)
                    });
                    const params = new URLSearchParams(window.location.search);
                    window.location.href = params.get('redirect') || 'catalogo.php';
                } else {
                    alertaError.textContent = datos.mensaje || 'Credenciales incorrectas.';
                    alertaError.classList.add('visible');
                }

            } catch (error) {
                alertaError.textContent = 'No se pudo conectar con el servidor. Verificá que Flask esté corriendo.';
                alertaError.classList.add('visible');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Ingresar';
            }
        });
    </script>

</body>
</html>