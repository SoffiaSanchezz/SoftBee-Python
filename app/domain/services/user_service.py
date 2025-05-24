from sqlalchemy.orm import Session
from app.domain.models.user_model import User
from app.core.security import get_password_hash
from fastapi import HTTPException

def crear_usuario(db: Session, user_data):
    # Verificar si el correo ya existe
    usuario_existente = db.query(User).filter(User.correo == user_data.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = get_password_hash(user_data.contraseña)
    nuevo_usuario = User(
        nombre=user_data.nombre,
        correo=user_data.correo,
        contraseña=hashed_password,
        direccion_apiario=user_data.direccion_apiario,
        cantidad_colmenas=user_data.cantidad_colmenas,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario
    