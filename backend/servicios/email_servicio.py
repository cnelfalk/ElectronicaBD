import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

# EmailServicio - gestiona el envío de correos electrónicos vía SMTP para TechMatch
class EmailServicio:

    # enviarCodigoRecuperacion - envía un email con el código de 6 dígitos al usuario
    def enviarCodigoRecuperacion(self, emailDestino, nombreUsuario, codigo):
        asunto = f"🔐 Tu código de recuperación — TechMatch"
        
        # construirHTML - arma el cuerpo del email con el diseño de TechMatch
        cuerpoHTML = self._construirTemplateEmail(nombreUsuario, codigo)
        
        return self._enviarEmail(emailDestino, asunto, cuerpoHTML)

    # _enviarEmail - se conecta al servidor SMTP y despacha el mensaje
    def _enviarEmail(self, destinatario, asunto, cuerpoHTML):
        try:
            mensaje = MIMEMultipart('alternative')
            mensaje['From'] = f"TechMatch <{Config.SMTP_EMAIL}>"
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto

            # adjuntarHTML - usa formato HTML para el cuerpo del email
            parteHTML = MIMEText(cuerpoHTML, 'html', 'utf-8')
            mensaje.attach(parteHTML)

            # conectarSMTP - establece conexión segura TLS con el servidor
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as servidor:
                servidor.ehlo()
                servidor.starttls()
                servidor.ehlo()
                servidor.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
                servidor.sendmail(Config.SMTP_EMAIL, destinatario, mensaje.as_string())

            print(f"// Email de recuperación enviado a: {destinatario}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"// errorSMTPAuth: Credenciales SMTP inválidas — {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"// errorSMTP: {e}")
            return False
        except Exception as e:
            print(f"// errorAlEnviarEmail: {e}")
            return False

    # _construirTemplateEmail - genera el HTML del correo con el estilo visual de TechMatch
    def _construirTemplateEmail(self, nombreUsuario, codigo):
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #0a0e17; font-family: 'Segoe UI', Arial, sans-serif;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0a0e17; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table role="presentation" width="480" cellspacing="0" cellpadding="0" style="background-color: #1a2332; border-radius: 16px; border: 1px solid rgba(148, 163, 184, 0.1); overflow: hidden;">
                            
                            <!-- Barra gradiente superior -->
                            <tr>
                                <td style="height: 4px; background: linear-gradient(135deg, #22d3ee, #6366f1);"></td>
                            </tr>

                            <!-- Logo -->
                            <tr>
                                <td style="padding: 28px 32px 16px; text-align: center;">
                                    <table role="presentation" cellspacing="0" cellpadding="0" style="margin: 0 auto;">
                                        <tr>
                                            <td style="width: 36px; height: 36px; background: linear-gradient(135deg, #22d3ee, #6366f1); border-radius: 8px; text-align: center; vertical-align: middle; font-size: 18px; font-weight: 900; color: #0a0e17;">T</td>
                                            <td style="padding-left: 10px; font-size: 22px; font-weight: 800; color: #22d3ee; letter-spacing: -0.5px;">TechMatch</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>

                            <!-- Contenido -->
                            <tr>
                                <td style="padding: 8px 32px 24px;">
                                    <h2 style="margin: 0 0 8px; color: #f1f5f9; font-size: 20px; font-weight: 700; text-align: center;">Recuperación de contraseña</h2>
                                    <p style="margin: 0 0 24px; color: #94a3b8; font-size: 15px; line-height: 1.6; text-align: center;">
                                        Hola <strong style="color: #f1f5f9;">{nombreUsuario}</strong>, recibimos una solicitud para restablecer tu contraseña. Usá el siguiente código:
                                    </p>

                                    <!-- Código OTP -->
                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td align="center" style="padding: 20px 0;">
                                                <div style="display: inline-block; background: rgba(34, 211, 238, 0.06); border: 2px solid rgba(34, 211, 238, 0.25); border-radius: 12px; padding: 16px 40px;">
                                                    <span style="font-size: 36px; font-weight: 800; letter-spacing: 12px; color: #22d3ee; font-family: 'Courier New', monospace;">{codigo}</span>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>

                                    <p style="margin: 16px 0 0; color: #64748b; font-size: 13px; text-align: center; line-height: 1.5;">
                                        ⏱️ Este código expira en <strong style="color: #94a3b8;">15 minutos</strong>.<br>
                                        Si no solicitaste este cambio, ignorá este correo.
                                    </p>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding: 16px 32px; border-top: 1px solid rgba(148, 163, 184, 0.08); text-align: center;">
                                    <p style="margin: 0; color: #475569; font-size: 12px;">
                                        © 2026 TechMatch — Comparador Inteligente de Hardware
                                    </p>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
