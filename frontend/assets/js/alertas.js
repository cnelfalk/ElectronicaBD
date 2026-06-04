// alertas.js - Modales personalizados de alerta y confirmación para TechMatch
(function() {
    // 1. Inyectar estilos CSS para los modales
    const style = document.createElement('style');
    style.innerHTML = `
        /* Fondo difuminado del modal */
        .tm-modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(6, 9, 15, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .tm-modal-backdrop.show {
            opacity: 1;
        }
        
        /* Contenedor del Modal */
        .tm-modal-box {
            background-color: var(--tm-bg-card, #1a2332);
            border: 1px solid rgba(34, 211, 238, 0.2);
            border-radius: var(--tm-radius-lg, 16px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(34, 211, 238, 0.05);
            width: 92%;
            max-width: 440px;
            overflow: hidden;
            transform: scale(0.92) translateY(10px);
            transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .tm-modal-backdrop.show .tm-modal-box {
            transform: scale(1) translateY(0);
        }
        
        /* Borde decorativo superior con degradado */
        .tm-modal-top-bar {
            height: 4px;
            background: var(--tm-accent-gradient, linear-gradient(135deg, #22d3ee, #6366f1));
            width: 100%;
        }
        
        /* Cabecera del Modal */
        .tm-modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.25rem 1.5rem 0.75rem;
            border-bottom: 1px solid var(--tm-border, rgba(148, 163, 184, 0.08));
        }
        
        /* Logo TechMatch en la cabecera */
        .tm-modal-logo {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--tm-text-primary, #f1f5f9);
            letter-spacing: -0.5px;
        }
        .tm-modal-logo-icon {
            width: 26px;
            height: 26px;
            background: var(--tm-accent-gradient, linear-gradient(135deg, #22d3ee, #6366f1));
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 900;
            color: var(--tm-bg-primary, #0a0e17);
        }
        .tm-modal-logo span {
            background: var(--tm-accent-gradient, linear-gradient(135deg, #22d3ee, #6366f1));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }
        
        /* Botón cerrar (X) */
        .tm-modal-close {
            background: transparent;
            border: none;
            color: var(--tm-text-muted, #64748b);
            font-size: 1.35rem;
            cursor: pointer;
            line-height: 1;
            padding: 0;
            transition: color 0.15s ease;
        }
        .tm-modal-close:hover {
            color: var(--tm-text-primary, #f1f5f9);
        }
        
        /* Cuerpo del Modal */
        .tm-modal-body {
            padding: 1.75rem 1.5rem;
            color: var(--tm-text-secondary, #94a3b8);
            font-size: 0.95rem;
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        /* Contenedor de Icono */
        .tm-modal-icon-wrapper {
            width: 54px;
            height: 54px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
            background: rgba(34, 211, 238, 0.06);
            border: 1px solid rgba(34, 211, 238, 0.15);
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.05);
        }
        .tm-modal-icon-wrapper.danger {
            background: rgba(239, 68, 68, 0.06);
            border-color: rgba(239, 68, 68, 0.2);
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.05);
        }
        .tm-modal-icon-wrapper.warning {
            background: rgba(251, 191, 36, 0.06);
            border-color: rgba(251, 191, 36, 0.2);
            box-shadow: 0 0 15px rgba(251, 191, 36, 0.05);
        }
        .tm-modal-icon-wrapper.success {
            background: rgba(34, 197, 94, 0.06);
            border-color: rgba(34, 197, 94, 0.2);
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.05);
        }
        
        /* Título del mensaje */
        .tm-modal-msg-title {
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--tm-text-primary, #f1f5f9);
            margin-bottom: 0.75rem;
        }
        
        /* Contenido del mensaje */
        .tm-modal-msg-text {
            color: var(--tm-text-secondary, #94a3b8);
            font-size: 0.92rem;
            margin: 0;
        }
        
        /* Pie del Modal / Botones */
        .tm-modal-footer {
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            padding: 1.25rem 1.5rem;
            border-top: 1px solid var(--tm-border, rgba(148, 163, 184, 0.08));
            background-color: rgba(10, 14, 23, 0.4);
        }
        
        /* Botones personalizados del modal */
        .tm-modal-btn {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            border-radius: var(--tm-radius-sm, 8px);
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            outline: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 110px;
        }
        
        /* Botón de Confirmación Principal */
        .tm-modal-btn-confirm {
            background: var(--tm-accent-gradient, linear-gradient(135deg, #22d3ee, #6366f1));
            color: var(--tm-bg-primary, #0a0e17) !important;
        }
        .tm-modal-btn-confirm:hover {
            background: var(--tm-accent-gradient-hover, linear-gradient(135deg, #06b6d4, #4f46e5));
            box-shadow: 0 4px 16px rgba(34, 211, 238, 0.35);
            transform: translateY(-1px);
        }
        .tm-modal-btn-confirm:active {
            transform: translateY(0);
        }
        
        /* Botón de Cancelación */
        .tm-modal-btn-cancel {
            background: transparent;
            color: var(--tm-text-secondary, #94a3b8);
            border: 1px solid var(--tm-border, rgba(148, 163, 184, 0.15));
        }
        .tm-modal-btn-cancel:hover {
            color: var(--tm-text-primary, #f1f5f9);
            border-color: var(--tm-text-secondary, #94a3b8);
            background: rgba(148, 163, 184, 0.05);
        }
        
        /* Botón de Acción Peligrosa (Eliminar) */
        .tm-modal-btn-danger {
            background: #ef4444;
            color: #ffffff !important;
        }
        .tm-modal-btn-danger:hover {
            background: #dc2626;
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.35);
            transform: translateY(-1px);
        }
        .tm-modal-btn-danger:active {
            transform: translateY(0);
        }
        
        /* Bloqueo de scroll del body */
        body.tm-modal-open {
            overflow: hidden;
            padding-right: var(--scrollbar-width, 0px);
        }
    `;
    document.head.appendChild(style);

    // Guardar el ancho de la barra de desplazamiento para evitar saltos de pantalla
    function setScrollbarWidth() {
        const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty('--scrollbar-width', `${scrollbarWidth}px`);
    }

    // 2. Función para crear y renderizar el modal en el DOM
    function renderCustomModal(type, message, resolve) {
        setScrollbarWidth();
        document.body.classList.add('tm-modal-open');

        const backdrop = document.createElement('div');
        backdrop.className = 'tm-modal-backdrop';
        
        const isConfirm = (type === 'confirm');
        let icon = '⚡';
        let title = 'TechMatch';
        let confirmText = 'Aceptar';
        let confirmBtnClass = 'tm-modal-btn-confirm';
        let iconClass = '';
        
        const msgLower = message.toLowerCase();
        
// Detección contextual para definir íconos y estilos
        if (msgLower.includes('eliminar') || msgLower.includes('quitar') || msgLower.includes('borrar')) {
            // Acción destructiva pura (Favoritos, Comparaciones)
            icon = '🗑️';
            title = 'Confirmar Acción';
            confirmText = 'Eliminar';
            confirmBtnClass = 'tm-modal-btn-danger';
            iconClass = 'danger';
        } else if (msgLower.includes('seguro') || msgLower.includes('salir') || msgLower.includes('cerrar sesión')) {
            // Confirmación general / Cerrar Sesión
            icon = '​❗​';
            title = 'Confirmar Acción';
            confirmText = 'Sí, continuar'; 
            confirmBtnClass = 'tm-modal-btn-danger'; // Lo mantenemos rojo para que destaque, o podés cambiarlo a tm-modal-btn-confirm
            iconClass = 'danger';
        } else if (msgLower.includes('no podés') || msgLower.includes('solo podés') || msgLower.includes('error') || msgLower.includes('falló') || msgLower.includes('incorrecto')) {
            // Alertas y errores
            icon = '⚠️';
            title = 'Atención';
            iconClass = 'warning';
        } else if (msgLower.includes('éxito') || msgLower.includes('guardado') || msgLower.includes('exitosamente') || msgLower.includes('agregado')) {
            // Éxito
            icon = '✨';
            title = '¡Excelente!';
            iconClass = 'success';
        }
        
        backdrop.innerHTML = `
            <div class="tm-modal-box">
                <div class="tm-modal-top-bar"></div>
                <div class="tm-modal-header">
                    <div class="tm-modal-logo">
                        <div class="tm-modal-logo-icon">T</div>
                        <span>TechMatch</span>
                    </div>
                    <button class="tm-modal-close" aria-label="Cerrar">&times;</button>
                </div>
                <div class="tm-modal-body">
                    <div class="tm-modal-icon-wrapper ${iconClass}">${icon}</div>
                    <h4 class="tm-modal-msg-title">${title}</h4>
                    <p class="tm-modal-msg-text">${message}</p>
                </div>
                <div class="tm-modal-footer">
                    ${isConfirm ? `<button class="tm-modal-btn tm-modal-btn-cancel tm-btn-cancel-action">Cancelar</button>` : ''}
                    <button class="tm-modal-btn ${confirmBtnClass} tm-btn-confirm-action">${confirmText}</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(backdrop);
        
        // Trigger de la animación
        setTimeout(() => backdrop.classList.add('show'), 10);
        
        // Soporte para tecla Escape y Enter
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                close(false);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                close(true);
            }
        };

        // Función para remover el modal
        function close(value) {
            backdrop.classList.remove('show');
            document.removeEventListener('keydown', handleKeyDown);
            setTimeout(() => {
                backdrop.remove();
                document.body.classList.remove('tm-modal-open');
                if (resolve) resolve(value);
            }, 250);
        }
        
        // Event Listeners
        backdrop.querySelector('.tm-btn-confirm-action').addEventListener('click', () => close(true));
        backdrop.querySelector('.tm-modal-close').addEventListener('click', () => close(false));
        if (isConfirm) {
            backdrop.querySelector('.tm-btn-cancel-action').addEventListener('click', () => close(false));
        }
        
        // Cerrar si se hace click en el fondo difuminado
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                close(false);
            }
        });

        document.addEventListener('keydown', handleKeyDown);
    }

    // 3. Sobrescribir el método alert por defecto del navegador
    window.alert = function(message) {
        return new Promise((resolve) => {
            renderCustomModal('alert', message, resolve);
        });
    };

    // 4. Crear método personalizado de confirmación asíncrona
    window.mostrarConfirmacion = function(message) {
        return new Promise((resolve) => {
            renderCustomModal('confirm', message, resolve);
        });
    };
})();
