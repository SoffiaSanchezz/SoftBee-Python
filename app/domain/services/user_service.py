from sqlalchemy.orm import Session
from app.domain.models.user_model import User, Apiario
from app.core.security import get_password_hash
from fastapi import HTTPException
from app.core.security import verify_password, create_access_token
from datetime import timedelta

def crear_usuario(db: Session, user_data):
    # Verificar si el correo ya existe
    usuario_existente = db.query(User).filter(User.correo == user_data.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = get_password_hash(user_data.contraseña)
    nuevo_usuario = User(
        nombre=user_data.nombre,
        correo=user_data.correo,
        contraseña=hashed_password
    )

    # Agregar los apiarios asociados
    for apiario_data in user_data.apiarios:
        apiario = Apiario(
            direccion=apiario_data.direccion,
            cantidad_colmenas=apiario_data.cantidad_colmenas,
            usuario=nuevo_usuario
        )
        db.add(apiario)  # Opcional: se puede omitir porque la relación los maneja

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def autenticar_usuario(db: Session, correo: str, contraseña: str):
    usuario = db.query(User).filter(User.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    if not verify_password(contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    # Si todo está correcto, crea el token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": usuario.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


