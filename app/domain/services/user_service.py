from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.security import get_password_hash, verify_password, create_access_token
from app.domain.models.user_model import User, Apiario
from app.domain.schemas.user_schema import UserCreate, UserResponse
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES

def crear_usuario(db: Session, user_data: UserCreate):
    # Verificar si el usuario ya existe
    usuario_existente = db.query(User).filter(User.correo == user_data.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Crear el usuario
    hashed_password = get_password_hash(user_data.contraseña)
    nuevo_usuario = User(
        nombre=user_data.nombre,
        telefono=user_data.telefono,
        correo=user_data.correo,
        contraseña=hashed_password
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    # Crear apiarios asociados si existen
    if user_data.apiarios:
        for apiario_data in user_data.apiarios:
            nuevo_apiario = Apiario(
                usuario_id=nuevo_usuario.id,
                nombre=apiario_data.nombre,
                direccion=apiario_data.direccion,
                cantidad_colmenas=apiario_data.cantidad_colmenas,
                latitud=apiario_data.latitud or "0",
                longitud=apiario_data.longitud or "0"
            )
            db.add(nuevo_apiario)
        
        db.commit()
        db.refresh(nuevo_usuario)
    
    return nuevo_usuario

def obtener_usuario_por_id(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

def obtener_todos_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def autenticar_usuario(db: Session, correo: str, contraseña: str):
    usuario = db.query(User).filter(User.correo == correo).first()
    
    # Primero verificamos si el usuario existe
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario no está registrado"
        )
    
    # Luego verificamos la contraseña
    if not verify_password(contraseña, usuario.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    access_token = create_access_token(
        data={"sub": usuario.correo},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}