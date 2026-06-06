<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMatch — Recuperar Contraseña</title>
    <meta name="description" content="Recuperá tu contraseña de TechMatch mediante un código enviado a tu correo electrónico.">
    <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        /* ── Estilos específicos para la página de recuperación ── */

        /* Contenedor de cada paso */
        .tm-recovery-step {
            display: none;
        }
        .tm-recovery-step.active {
            display: block;
        }

        /* Header con icono del paso */
        .tm-recovery-icon {
            width: 56px;
            height: 56px;
            margin: 0 auto 1.25rem;
            border-radius: 50%;
            background: rgba(34, 211, 238, 0.06);
            border: 1px solid rgba(34, 211, 238, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
        }

        /* Indicador de pasos (1 — 2 — 3) */
        .tm-steps-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 1.75rem;
        }
        .tm-step-dot {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.78rem;
            font-weight: 700;
            border: 2px solid var(--tm-border);
            color: var(--tm-text-muted);
            transition: all 0.3s ease;
        }
        .tm-step-dot.active {
            background: var(--tm-accent-gradient);
            border-color: transparent;
            color: var(--tm-bg-primary);
        }
        .tm-step-dot.completed {
            background: rgba(34, 197, 94, 0.15);
            border-color: rgba(34, 197, 94, 0.4);
            color: #34d399;
        }
        .tm-step-line {
            width: 40px;
            height: 2px;
            background: var(--tm-border);
            transition: background 0.3s ease;
        }
        .tm-step-line.active {
            background: var(--tm-accent);
        }

        /* Inputs OTP (código de 6 dígitos) */
        .tm-otp-container {
            display: flex;
            justify-content: center;
            gap: 0.6rem;
            margin: 1.25rem 0;
        }
        .tm-otp-input {
            width: 48px;
            height: 56px;
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            background: var(--tm-bg-surface);
            border: 2px solid var(--tm-border);
            border-radius: var(--tm-radius-sm);
            color: var(--tm-text-primary);
            outline: none;
            transition: all 0.2s ease;
            caret-color: var(--tm-accent);
        }
        .tm-otp-input:focus {
            border-color: var(--tm-accent);
            box-shadow: 0 0 0 3px var(--tm-accent-glow);
        }
        .tm-otp-input.filled {
            border-color: var(--tm-accent);
            background: rgba(34, 211, 238, 0.04);
        }

        /* Timer de reenvío */
        .tm-resend-timer {
            text-align: center;
            font-size: 0.82rem;
            color: var(--tm-text-muted);
            margin-top: 1rem;
        }
        .tm-resend-link {
            color: var(--tm-accent) !important;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
        }
        .tm-resend-link:hover {
            text-decoration: underline;
        }
        .tm-resend-link.disabled {
            color: var(--tm-text-muted) !important;
            cursor: not-allowed;
            pointer-events: none;
        }

        /* Indicador de fuerza de contraseña */
        .tm-password-strength {
            height: 4px;
            border-radius: 2px;
            background: var(--tm-border);
            margin-top: 0.5rem;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .tm-password-strength-bar {
            height: 100%;
            border-radius: 2px;
            width: 0%;
            transition: all 0.3s ease;
        }
        .tm-password-strength-text {
            font-size: 0.75rem;
            margin-top: 0.3rem;
            transition: color 0.3s ease;
        }

        /* Email mostrado como badge */
        .tm-email-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.85rem;
            background: rgba(34, 211, 238, 0.06);
            border: 1px solid rgba(34, 211, 238, 0.15);
            border-radius: 50px;
            font-size: 0.82rem;
            color: var(--tm-accent);
            font-weight: 500;
            margin: 0.5rem 0 0.75rem;
            word-break: break-all;
        }

        /* Éxito final */
        .tm-success-check {
            width: 64px;
            height: 64px;
            margin: 0 auto 1.25rem;
            border-radius: 50%;
            background: rgba(34, 197, 94, 0.1);
            border: 2px solid rgba(34, 197, 94, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
        }
    </style>
</head>
<body>

    <?php include 'componentes/navbar.php'; ?>

    <div class="tm-auth-wrapper">
        <div class="tm-auth-card" style="max-width: 460px;">

            <!-- Indicador de pasos -->
            <div class="tm-steps-indicator" id="stepsIndicator">
                <div class="tm-step-dot active" id="stepDot1">1</div>
                <div class="tm-step-line" id="stepLine1"></div>
                <div class="tm-step-dot" id="stepDot2">2</div>
                <div class="tm-step-line" id="stepLine2"></div>
                <div class="tm-step-dot" id="stepDot3">3</div>
            </div>

            <!-- Alertas -->
            <div id="alerta-error" class="tm-alert tm-alert-error"></div>
            <div id="alerta-exito" class="tm-alert tm-alert-success"></div>

            <!-- ═══════════════════════════════════════ -->
            <!-- PASO 1: Ingresar email                 -->
            <!-- ═══════════════════════════════════════ -->
            <div class="tm-recovery-step active" id="paso1">
                <div class="tm-recovery-icon">📧</div>
                <h2 style="text-align: center; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.4rem;">
                    Recuperá tu contraseña
                </h2>
                <p class="tm-subtitle" style="text-align: center; margin-bottom: 1.5rem;">
                    Ingresá el correo electrónico con el que te registraste y te enviaremos un código de verificación.
                </p>

                <form id="form-email">
                    <div class="tm-form-group">
                        <label for="emailRecuperacion">Correo electrónico</label>
                        <input type="email" class="tm-input" id="emailRecuperacion" placeholder="tu@email.com" required>
                    </div>
                    <button type="submit" class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg" id="btn-enviar-codigo">
                        Enviar código
                    </button>
                </form>

                <hr class="tm-divider">
                <p class="tm-auth-footer">
                    <a href="login.php">← Volver al inicio de sesión</a>
                </p>
            </div>

            <!-- ═══════════════════════════════════════ -->
            <!-- PASO 2: Ingresar código OTP             -->
            <!-- ═══════════════════════════════════════ -->
            <div class="tm-recovery-step" id="paso2">
                <div class="tm-recovery-icon">🔐</div>
                <h2 style="text-align: center; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.4rem;">
                    Ingresá el código
                </h2>
                <p class="tm-subtitle" style="text-align: center;">
                    Enviamos un código de 6 dígitos a:
                </p>
                <div style="text-align: center;">
                    <span class="tm-email-badge" id="emailMostrado">correo@ejemplo.com</span>
                </div>

                <div class="tm-otp-container" id="otpContainer">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="0" autocomplete="one-time-code">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="1">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="2">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="3">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="4">
                    <input type="text" class="tm-otp-input" maxlength="1" inputmode="numeric" pattern="[0-9]" data-index="5">
                </div>

                <button class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg" id="btn-verificar-codigo" disabled>
                    Verificar código
                </button>

                <div class="tm-resend-timer" id="resendTimer">
                    ¿No recibiste el código? <span class="tm-resend-link disabled" id="btnReenviar">Reenviar (<span id="timerCount">60</span>s)</span>
                </div>

                <hr class="tm-divider">
                <p class="tm-auth-footer">
                    <a href="#" id="btnVolverPaso1">← Cambiar correo electrónico</a>
                </p>
            </div>

            <!-- ═══════════════════════════════════════ -->
            <!-- PASO 3: Nueva contraseña               -->
            <!-- ═══════════════════════════════════════ -->
            <div class="tm-recovery-step" id="paso3">
                <div class="tm-recovery-icon">🔑</div>
                <h2 style="text-align: center; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.4rem;">
                    Creá tu nueva contraseña
                </h2>
                <p class="tm-subtitle" style="text-align: center; margin-bottom: 1.5rem;">
                    Elegí una contraseña segura de al menos 6 caracteres.
                </p>

                <form id="form-nueva-contrasenia">
                    <div class="tm-form-group">
                        <label for="nuevaContrasenia">Nueva contraseña</label>
                        <input type="password" class="tm-input" id="nuevaContrasenia" placeholder="Mínimo 6 caracteres" required minlength="6">
                        <div class="tm-password-strength">
                            <div class="tm-password-strength-bar" id="strengthBar"></div>
                        </div>
                        <div class="tm-password-strength-text" id="strengthText" style="color: var(--tm-text-muted);"></div>
                    </div>
                    <div class="tm-form-group">
                        <label for="confirmarContrasenia">Confirmar contraseña</label>
                        <input type="password" class="tm-input" id="confirmarContrasenia" placeholder="Repetí la contraseña" required minlength="6">
                    </div>
                    <button type="submit" class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg" id="btn-cambiar-contrasenia">
                        Cambiar contraseña
                    </button>
                </form>
            </div>

            <!-- ═══════════════════════════════════════ -->
            <!-- PASO FINAL: Éxito                      -->
            <!-- ═══════════════════════════════════════ -->
            <div class="tm-recovery-step" id="pasoExito">
                <div class="tm-success-check">✅</div>
                <h2 style="text-align: center; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.4rem;">
                    ¡Contraseña actualizada!
                </h2>
                <p class="tm-subtitle" style="text-align: center; margin-bottom: 1.5rem;">
                    Tu contraseña fue cambiada exitosamente. Ya podés iniciar sesión con tu nueva contraseña.
                </p>
                <a href="login.php" class="tm-btn tm-btn-primary tm-btn-w-full tm-btn-lg">
                    Ir a Iniciar Sesión
                </a>
            </div>

        </div>
    </div>

    <?php include 'componentes/footer.php'; ?>

    <script src="assets/js/api.js"></script>
    <script>
        // ══════════════════════════════════════════
        //  Estado global del flujo de recuperación
        // ══════════════════════════════════════════
        let emailUsuario = '';
        let tokenVerificacion = '';
        let timerInterval = null;

        // Referencias DOM
        const alertaError = document.getElementById('alerta-error');
        const alertaExito = document.getElementById('alerta-exito');

        // ── Utilidades de UI ──
        function mostrarError(msg) {
            alertaExito.classList.remove('visible');
            alertaError.textContent = msg;
            alertaError.classList.add('visible');
        }
        function mostrarExito(msg) {
            alertaError.classList.remove('visible');
            alertaExito.textContent = msg;
            alertaExito.classList.add('visible');
        }
        function limpiarAlertas() {
            alertaError.classList.remove('visible');
            alertaExito.classList.remove('visible');
        }

        // ── Navegación entre pasos ──
        function irAPaso(numeroPaso) {
            document.querySelectorAll('.tm-recovery-step').forEach(s => s.classList.remove('active'));
            limpiarAlertas();

            if (numeroPaso === 1) document.getElementById('paso1').classList.add('active');
            else if (numeroPaso === 2) document.getElementById('paso2').classList.add('active');
            else if (numeroPaso === 3) document.getElementById('paso3').classList.add('active');
            else if (numeroPaso === 4) document.getElementById('pasoExito').classList.add('active');

            // Actualizar indicador de pasos
            for (let i = 1; i <= 3; i++) {
                const dot = document.getElementById(`stepDot${i}`);
                const line = i < 3 ? document.getElementById(`stepLine${i}`) : null;

                dot.classList.remove('active', 'completed');
                if (line) line.classList.remove('active');

                if (i < numeroPaso || numeroPaso === 4) {
                    dot.classList.add('completed');
                    dot.innerHTML = '✓';
                    if (line) line.classList.add('active');
                } else if (i === numeroPaso) {
                    dot.classList.add('active');
                    dot.textContent = i;
                } else {
                    dot.textContent = i;
                }
            }
        }

        // ══════════════════════════════════════════
        //  PASO 1: Enviar código al email
        // ══════════════════════════════════════════
        document.getElementById('form-email').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('btn-enviar-codigo');
            emailUsuario = document.getElementById('emailRecuperacion').value.trim();

            btn.disabled = true;
            btn.textContent = 'Enviando...';
            limpiarAlertas();

            try {
                const resp = await fetch(`${API_URL}/recuperar/solicitar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ emailUsuario })
                });
                const datos = await resp.json();

                if (datos.success) {
                    document.getElementById('emailMostrado').textContent = emailUsuario;
                    irAPaso(2);
                    iniciarTimerReenvio();
                    // Hacer focus en el primer input OTP
                    document.querySelector('.tm-otp-input').focus();
                } else {
                    mostrarError(datos.mensaje || 'Error al enviar el código.');
                }
            } catch (error) {
                mostrarError('No se pudo conectar con el servidor.');
            } finally {
                btn.disabled = false;
                btn.textContent = 'Enviar código';
            }
        });

        // ══════════════════════════════════════════
        //  PASO 2: Inputs OTP y verificación
        // ══════════════════════════════════════════
        const otpInputs = document.querySelectorAll('.tm-otp-input');
        const btnVerificar = document.getElementById('btn-verificar-codigo');

        // Manejar escritura, pegado y navegación entre inputs OTP
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => {
                const valor = e.target.value;

                // Sólo permitir números
                if (!/^\d$/.test(valor)) {
                    e.target.value = '';
                    return;
                }

                e.target.classList.add('filled');

                // Avanzar al siguiente input
                if (index < 5) {
                    otpInputs[index + 1].focus();
                }

                verificarOTPCompleto();
            });

            input.addEventListener('keydown', (e) => {
                // Retroceder con Backspace
                if (e.key === 'Backspace' && !e.target.value && index > 0) {
                    otpInputs[index - 1].focus();
                    otpInputs[index - 1].value = '';
                    otpInputs[index - 1].classList.remove('filled');
                }
            });

            // Soporte para pegar código completo
            input.addEventListener('paste', (e) => {
                e.preventDefault();
                const texto = (e.clipboardData || window.clipboardData).getData('text').trim();
                if (/^\d{6}$/.test(texto)) {
                    texto.split('').forEach((digito, i) => {
                        otpInputs[i].value = digito;
                        otpInputs[i].classList.add('filled');
                    });
                    otpInputs[5].focus();
                    verificarOTPCompleto();
                }
            });

            // Seleccionar todo el contenido al enfocar
            input.addEventListener('focus', () => input.select());
        });

        function verificarOTPCompleto() {
            const codigo = Array.from(otpInputs).map(i => i.value).join('');
            btnVerificar.disabled = codigo.length !== 6;
        }

        // Enviar código al backend
        btnVerificar.addEventListener('click', async () => {
            const codigo = Array.from(otpInputs).map(i => i.value).join('');
            btnVerificar.disabled = true;
            btnVerificar.textContent = 'Verificando...';
            limpiarAlertas();

            try {
                const resp = await fetch(`${API_URL}/recuperar/verificar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ emailUsuario, codigo })
                });
                const datos = await resp.json();

                if (datos.success) {
                    tokenVerificacion = datos.token;
                    irAPaso(3);
                    document.getElementById('nuevaContrasenia').focus();
                } else {
                    mostrarError(datos.mensaje || 'Código inválido.');
                    // Limpiar inputs OTP
                    otpInputs.forEach(i => { i.value = ''; i.classList.remove('filled'); });
                    otpInputs[0].focus();
                }
            } catch (error) {
                mostrarError('No se pudo conectar con el servidor.');
            } finally {
                btnVerificar.disabled = false;
                btnVerificar.textContent = 'Verificar código';
                verificarOTPCompleto();
            }
        });

        // Timer de reenvío (60 segundos)
        function iniciarTimerReenvio() {
            let segundos = 60;
            const btnReenviar = document.getElementById('btnReenviar');
            const timerCount = document.getElementById('timerCount');

            btnReenviar.classList.add('disabled');
            timerCount.textContent = segundos;
            btnReenviar.innerHTML = `Reenviar (<span id="timerCount">${segundos}</span>s)`;

            if (timerInterval) clearInterval(timerInterval);

            timerInterval = setInterval(() => {
                segundos--;
                const countEl = document.getElementById('timerCount');
                if (countEl) countEl.textContent = segundos;

                if (segundos <= 0) {
                    clearInterval(timerInterval);
                    btnReenviar.classList.remove('disabled');
                    btnReenviar.textContent = 'Reenviar código';
                }
            }, 1000);
        }

        // Reenviar código
        document.getElementById('btnReenviar').addEventListener('click', async (e) => {
            e.preventDefault();
            if (e.target.classList.contains('disabled')) return;

            limpiarAlertas();
            try {
                const resp = await fetch(`${API_URL}/recuperar/solicitar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ emailUsuario })
                });
                const datos = await resp.json();
                if (datos.success) {
                    mostrarExito('Código reenviado. Revisá tu bandeja de entrada.');
                    iniciarTimerReenvio();
                    otpInputs.forEach(i => { i.value = ''; i.classList.remove('filled'); });
                    otpInputs[0].focus();
                }
            } catch (error) {
                mostrarError('Error al reenviar el código.');
            }
        });

        // Volver al paso 1
        document.getElementById('btnVolverPaso1').addEventListener('click', (e) => {
            e.preventDefault();
            if (timerInterval) clearInterval(timerInterval);
            irAPaso(1);
        });

        // ══════════════════════════════════════════
        //  PASO 3: Nueva contraseña
        // ══════════════════════════════════════════

        // Indicador de fuerza de contraseña
        document.getElementById('nuevaContrasenia').addEventListener('input', (e) => {
            const password = e.target.value;
            const bar = document.getElementById('strengthBar');
            const text = document.getElementById('strengthText');
            let score = 0;
            let label = '';
            let color = '';

            if (password.length >= 6) score++;
            if (password.length >= 10) score++;
            if (/[A-Z]/.test(password)) score++;
            if (/[0-9]/.test(password)) score++;
            if (/[^A-Za-z0-9]/.test(password)) score++;

            if (password.length === 0) {
                bar.style.width = '0%';
                text.textContent = '';
                return;
            }

            if (score <= 1) { label = 'Débil'; color = '#ef4444'; bar.style.width = '20%'; }
            else if (score <= 2) { label = 'Regular'; color = '#f59e0b'; bar.style.width = '40%'; }
            else if (score <= 3) { label = 'Buena'; color = '#22d3ee'; bar.style.width = '65%'; }
            else { label = 'Fuerte'; color = '#22c55e'; bar.style.width = '90%'; }

            bar.style.background = color;
            text.style.color = color;
            text.textContent = label;
        });

        // Enviar nueva contraseña
        document.getElementById('form-nueva-contrasenia').addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('btn-cambiar-contrasenia');
            const nueva = document.getElementById('nuevaContrasenia').value;
            const confirmar = document.getElementById('confirmarContrasenia').value;

            limpiarAlertas();

            if (nueva !== confirmar) {
                mostrarError('Las contraseñas no coinciden.');
                return;
            }

            if (nueva.length < 6) {
                mostrarError('La contraseña debe tener al menos 6 caracteres.');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Actualizando...';

            try {
                const resp = await fetch(`${API_URL}/recuperar/cambiar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        emailUsuario,
                        token: tokenVerificacion,
                        nuevaContrasenia: nueva
                    })
                });
                const datos = await resp.json();

                if (datos.success) {
                    irAPaso(4);
                } else {
                    mostrarError(datos.mensaje || 'Error al cambiar la contraseña.');
                }
            } catch (error) {
                mostrarError('No se pudo conectar con el servidor.');
            } finally {
                btn.disabled = false;
                btn.textContent = 'Cambiar contraseña';
            }
        });

        // Si el usuario ya está logueado, redirigir
        if (localStorage.getItem('techmatch_usuario')) {
            window.location.href = 'catalogo.php';
        }
    </script>

</body>
</html>
