<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Crear Cuenta</title>
    <meta name="description" content="Creá tu cuenta en TechMatch para guardar favoritos y comparar hardware.">
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <div class="tm-auth-wrapper">
        <div class="tm-auth-card">
            <h2>Crear Cuenta</h2>
            <p class="tm-subtitle">Registrate para guardar favoritos y comparaciones</p>

            <div id="alerta-error" class="tm-alert tm-alert-error"></div>
            <div id="alerta-exito" class="tm-alert tm-alert-success"></div>

            <form id="form-registro">
                <div class="tm-form-group">
                    <label for="nombre">Nombre de usuario</label>
                    <input type="text" class="tm-input" id="nombre" placeholder="Tu nombre" required maxlength="30">
                </div>
                <div class="tm-form-group">
                    <label for="email">Correo electrónico</label>
                    <input type="email" class="tm-input" id="email" placeholder="tu@email.com" required maxlength="150">
                </div>
                <div class="tm-form-group">
                    <label for="contrasenia">Contraseña</label>
                    <div class="tm-password-wrapper">
                        <input type="password" class="tm-input" id="contrasenia" placeholder="Mínimo 6 caracteres" required minlength="6" maxlength="255">
                        <button type="button" class="tm-password-toggle" onclick="togglePasswordVisibility('contrasenia', this)" aria-label="Mostrar/ocultar contraseña">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                                <line class="eye-slash" x1="3" y1="3" x2="21" y2="21"></line>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="tm-form-group">
                    <label for="confirmar">Confirmar contraseña</label>
                    <div class="tm-password-wrapper">
                        <input type="password" class="tm-input" id="confirmar" placeholder="Repetí la contraseña" required maxlength="255">
                        <button type="button" class="tm-password-toggle" onclick="togglePasswordVisibility('confirmar', this)" aria-label="Mostrar/ocultar contraseña">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                                <line class="eye-slash" x1="3" y1="3" x2="21" y2="21"></line>
                            </svg>
                        </button>
                    </div>
                </div>
                <button type="submit" class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg" id="btn-submit">
                    Crear cuenta
                </button>
            </form>

            <hr class="tm-divider">
            <p class="tm-auth-footer">
                ¿Ya tenés cuenta? <a href="login.php">Iniciá sesión</a>
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

        document.getElementById('form-registro').addEventListener('submit', async function (e) {
            e.preventDefault();

            const btnSubmit = document.getElementById('btn-submit');
            const alertaError = document.getElementById('alerta-error');
            const alertaExito = document.getElementById('alerta-exito');

            alertaError.classList.remove('visible');
            alertaExito.classList.remove('visible');

            const nombre = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const contrasenia = document.getElementById('contrasenia').value;
            const confirmar = document.getElementById('confirmar').value;

            if (contrasenia !== confirmar) {
                alertaError.textContent = 'Las contraseñas no coinciden.';
                alertaError.classList.add('visible');
                return;
            }



            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Creando cuenta...';

            try {
                const respuesta = await fetch(`${API_URL}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        nombreUsuario: nombre,
                        emailUsuario: email,
                        contraseniaUsuario: contrasenia
                    })
                });

                const datos = await respuesta.json();

                if (datos.success) {
                    alertaExito.textContent = '¡Cuenta creada! Redirigiendo al inicio de sesión...';
                    alertaExito.classList.add('visible');
                    setTimeout(() => {
                        window.location.href = 'login.php';
                    }, 2000);
                } else {
                    alertaError.textContent = datos.mensaje || 'No se pudo crear la cuenta.';
                    alertaError.classList.add('visible');
                }

            } catch (error) {
                console.error('Error en registro:', error);
                alertaError.textContent = 'No se pudo conectar con el servidor. Verificá que Flask esté corriendo.';
                alertaError.classList.add('visible');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Crear cuenta';
            }
        });
    </script>

</body>
</html>
