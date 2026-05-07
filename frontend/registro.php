<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch - Registrarse</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="bg-light">

    <?php include 'componentes/navbar.php'; ?>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <h4 class="card-title mb-4 text-center">Crear Cuenta</h4>

                        <div id="alerta-error" class="alert alert-danger d-none" role="alert"></div>
                        <div id="alerta-exito" class="alert alert-success d-none" role="alert"></div>

                        <form id="form-registro">
                            <div class="mb-3">
                                <label for="nombre" class="form-label">Nombre de usuario</label>
                                <input type="text" class="form-control" id="nombre" placeholder="Tu nombre" required>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Correo electrónico</label>
                                <input type="email" class="form-control" id="email" placeholder="tu@email.com" required>
                            </div>
                            <div class="mb-3">
                                <label for="contrasenia" class="form-label">Contraseña</label>
                                <input type="password" class="form-control" id="contrasenia" placeholder="Mínimo 6 caracteres" required minlength="6">
                            </div>
                            <div class="mb-3">
                                <label for="confirmar" class="form-label">Confirmar contraseña</label>
                                <input type="password" class="form-control" id="confirmar" placeholder="Repetí la contraseña" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100" id="btn-submit">
                                Crear cuenta
                            </button>
                        </form>

                        <hr>
                        <p class="text-center mb-0 small">
                            ¿Ya tenés cuenta? <a href="login.php">Iniciá sesión</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_URL = 'http://100.82.23.52:5000/api';

        // Si ya está logueado, redirigir directo al catálogo
        if (localStorage.getItem('techmatch_usuario')) {
            window.location.href = 'catalogo.php';
        }

        document.getElementById('form-registro').addEventListener('submit', async function (e) {
            e.preventDefault();

            const btnSubmit = document.getElementById('btn-submit');
            const alertaError = document.getElementById('alerta-error');
            const alertaExito = document.getElementById('alerta-exito');

            alertaError.classList.add('d-none');
            alertaExito.classList.add('d-none');

            const nombre = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const contrasenia = document.getElementById('contrasenia').value;
            const confirmar = document.getElementById('confirmar').value;

            // Validación client-side antes de llamar a la API
            if (contrasenia !== confirmar) {
                alertaError.textContent = 'Las contraseñas no coinciden.';
                alertaError.classList.remove('d-none');
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
                    alertaExito.classList.remove('d-none');
                    setTimeout(() => {
                        window.location.href = 'login.php';
                    }, 2000);
                } else {
                    alertaError.textContent = datos.mensaje || 'No se pudo crear la cuenta.';
                    alertaError.classList.remove('d-none');
                }

            } catch (error) {
                alertaError.textContent = 'No se pudo conectar con el servidor. Verificá que Flask esté corriendo.';
                alertaError.classList.remove('d-none');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Crear cuenta';
            }
        });
    </script>

</body>
</html>
