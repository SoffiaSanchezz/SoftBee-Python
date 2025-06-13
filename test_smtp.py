import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Configuración SMTP
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # Asegúrate de que sea un entero
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Crear mensaje de prueba
msg = MIMEText("¡Este es un correo de prueba desde Python!")
msg["Subject"] = "Prueba SMTP"
msg["From"] = SMTP_USER
msg["To"] = SMTP_USER  # Enviar a ti mismo

try:
    # Iniciar conexión SMTP
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()  # Usar TLS (necesario para puerto 587)
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    print("✅ Correo enviado correctamente. Revisa tu bandeja de entrada (o spam).")
except Exception as e:
    print(f"❌ Error al enviar el correo: {e}")