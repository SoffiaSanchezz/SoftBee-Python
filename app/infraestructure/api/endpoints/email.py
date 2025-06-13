from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from fastapi import HTTPException, status

def send_reset_email(email: str, token: str):
    try:
        reset_url = f"{settings.FRONTEND_URL}/#/reset-password?token={token}"
        
        # Logs para depuración
        print(f"URL de reset generada: {reset_url}")
        print(f"Intentando enviar correo a {email} con token {token}")
        print(f"Usando SMTP_USER: {settings.SMTP_USER}")
        
        # Crear mensaje de correo
        message = MIMEMultipart()
        message["From"] = settings.SMTP_USER
        message["To"] = email
        message["Subject"] = "Restablecer tu contraseña - SoftBee"
        
        # Cuerpo del correo en HTML
        body = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                
                <!-- Encabezado -->
                <div style="background: linear-gradient(135deg, #FFC107, #FFB300); padding: 40px 30px; text-align: center;">
                    <div style="width: 70px; height: 70px; border-radius: 50%; background-color: rgba(255, 255, 255, 0.15); margin: auto; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 32px;">🐝</span>
                    </div>
                    <h1 style="color: white; font-size: 28px; font-weight: bold; margin: 20px 0 0;">SoftBee</h1>
                </div>

                <!-- Contenido principal -->
                <div style="padding: 40px 30px; text-align: center;">
                    <h2 style="color: #1a202c; font-size: 24px; font-weight: 600;">Restablecer contraseña</h2>
                    <p style="color: #4a5568; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                        Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.
                    </p>
                    <p style="color: #4a5568; font-size: 16px; margin-bottom: 30px;">
                        Haz clic en el siguiente botón para continuar:
                    </p>

                    <!-- Botón -->
                    <div style="margin: 30px 0;">
                        <a href="{reset_url}"
                           style="display: inline-block;
                                  background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%);
                                  color: white;
                                  padding: 16px 32px;
                                  text-decoration: none;
                                  border-radius: 50px;
                                  font-weight: 600;
                                  font-size: 16px;
                                  box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
                                  letter-spacing: 0.5px;">
                            Restablecer contraseña
                        </a>
                    </div>

                    <!-- Información adicional -->
                    <div style="background-color: #f7fafc; border-left: 4px solid #FFC107; padding: 20px; border-radius: 8px; margin: 30px 0;">
                        <p style="color: #2d3748; font-weight: bold; margin-bottom: 10px;">⚠️ Información importante:</p>
                        <p style="color: #4a5568; margin-bottom: 5px;">• Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
                        <p style="color: #4a5568;">• El enlace expirará en 1 hora.</p>
                    </div>

                    <!-- Enlace alternativo -->
                    <div style="background-color: #edf2f7; padding: 15px; border-radius: 8px; margin-top: 20px;">
                        <p style="color: #718096; font-size: 12px; font-weight: 600; margin-bottom: 8px;">¿No funciona el botón? Copia este enlace:</p>
                        <p style="word-break: break-all; color: #4a5568; font-size: 12px; background-color: white; padding: 8px; border-radius: 4px;">
                            {reset_url}
                        </p>
                    </div>
                </div>

                <!-- Footer -->
                <div style="background-color: #2d3748; padding: 25px 30px; text-align: center;">
                    <h3 style="color: #FFC107; margin: 0 0 5px; font-size: 18px;">🐝 SoftBee</h3>
                    <p style="color: #a0aec0; font-size: 13px; margin: 0;">Tu plataforma de confianza</p>
                    <hr style="border: none; border-top: 1px solid #4a5568; margin: 15px 0;">
                    <p style="color: #718096; font-size: 11px; margin: 0;">© {datetime.now().year} SoftBee. Todos los derechos reservados.</p>
                    <p style="color: #718096; font-size: 11px; margin: 0;">Este es un correo automático, no respondas a este mensaje.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Adjuntar el cuerpo HTML al mensaje
        message.attach(MIMEText(body, "html"))

        # Enviar el correo
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar el correo de recuperación: {str(e)}"
        )
