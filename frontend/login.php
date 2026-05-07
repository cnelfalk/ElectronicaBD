<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch - Iniciar Sesión</title>
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
                        <h4 class="card-title mb-4 text-center">Iniciar Sesión</h4>

                        <div id="alerta-error" class="alert alert-danger d-none" role="alert"></div>

                        <form id="form-login">
                            <div class="mb-3">
                                <label for="email" class="form-label">Correo electrónico</label>
                                <input type="email" class="form-control" id="email" placeholder="tu@email.com" required>
                            </div>
                            <div class="mb-3">
                                <label for="contrasenia" class="form-label">Contraseña</label>
                                <input type="password" class="form-control" id="contrasenia" placeholder="Tu contraseña" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100" id="btn-submit">
                                Ingresar
                            </button>
                        </form>

                        <hr>
                        <p class="text-center mb-0 small">
                            ¿No tenés cuenta? <a href="registro.php">Registrate acá</a>
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

        document.getElementById('form-login').addEventListener('submit', async function (e) {
            e.preventDefault();

            const btnSubmit = document.getElementById('btn-submit');
            const alertaError = document.getElementById('alerta-error');

            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Ingresando...';
            alertaError.classList.add('d-none');

            const email = document.getElementById('email').value.trim();
            const contrasenia = document.getElementById('contrasenia').value;

            try {
                const respuesta = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        emailUsuario: email,
                        contraseniaUsuario: contrasenia
                    })
                });

                const datos = await respuesta.json();

                if (datos.success) {
                    localStorage.setItem('techmatch_usuario', JSON.stringify(datos.datos));

                    // Volver a la página desde donde vino (si aplica), o al catálogo
                    const params = new URLSearchParams(window.location.search);
                    window.location.href = params.get('redirect') || 'catalogo.php';
                } else {
                    alertaError.textContent = datos.mensaje || 'Credenciales incorrectas.';
                    alertaError.classList.remove('d-none');
                }

            } catch (error) {
                alertaError.textContent = 'No se pudo conectar con el servidor. Verificá que Flask esté corriendo.';
                alertaError.classList.remove('d-none');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Ingresar';
            }
        });
    </script>

</body>
</html>
