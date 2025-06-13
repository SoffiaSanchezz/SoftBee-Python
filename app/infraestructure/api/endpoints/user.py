from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from app.domain.schemas.user_schema import (
    UserCreate, UserResponse, UserLogin, Token,
    PasswordResetRequest, PasswordReset, PasswordResetResponse
)

from app.infraestructure.database.session import get_db
from app.core.security import get_current_user, create_access_token
from app.domain.models.user_model import User
from app.domain.services.user_service import (
    crear_usuario,
    autenticar_usuario,
    obtener_usuario_por_id,
    obtener_todos_usuarios
)
from app.domain.services.password_service import (
    request_password_reset,
    reset_password
)
from app.core.config import settings

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    responses={404: {"description": "No encontrado"}}
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Validación adicional: asegurar que hay al menos un apiario
        if not user.apiarios:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requiere al menos un apiario"
            )
            
        usuario_creado = crear_usuario(db, user)
        return usuario_creado
        
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    return autenticar_usuario(db, credentials.correo, credentials.contraseña)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    return obtener_todos_usuarios(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return obtener_usuario_por_id(db, user_id)

@router.post("/forgot-password", response_model=PasswordResetResponse)
async def forgot_password(
    request: PasswordResetRequest, 
    db: Session = Depends(get_db)
):
    return request_password_reset(db, request.correo)

@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password_endpoint(
    reset_data: PasswordReset, 
    db: Session = Depends(get_db)
):
    return reset_password(db, reset_data.token, reset_data.nueva_contraseña)
