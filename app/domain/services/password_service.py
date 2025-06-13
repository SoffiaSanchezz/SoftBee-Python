import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.domain.models.user_model import User
from app.infraestructure.api.endpoints.email import send_reset_email
from app.core.config import settings

def request_password_reset(db: Session, correo: str):
    user = db.query(User).filter(User.correo == correo).first()
    if not user:
        # Por seguridad no revelamos si el correo existe
        return {"message": "Si el correo existe, se ha enviado un enlace de recuperación"}
    
    # Generar token y fecha de expiración (1 hora)
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    
    user.reset_token = token
    user.reset_token_expires = expires
    db.commit()
    
    # Enviar correo
    try:
        send_reset_email(user.correo, token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar el correo: {str(e)}"
        )
    
    return {"message": "Si el correo existe, se ha enviado un enlace de recuperación"}

def reset_password(db: Session, token: str, nueva_contraseña: str):
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    user.contraseña = get_password_hash(nueva_contraseña)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}