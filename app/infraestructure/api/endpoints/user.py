from app.domain.services.user_service import crear_usuario, autenticar_usuario
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.schemas.user_schema import UserCreate
from app.infraestructure.database.session import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
router = APIRouter(prefix="/users", tags=["users"])

# Registro
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        nuevo_usuario = crear_usuario(db, user)
        return {"msg": "Usuario registrado exitosamente", "correo": nuevo_usuario.correo}
    except ValueError as ve:
        # Supongamos que crear_usuario lanza un ValueError si el correo ya existe
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Login
class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str

@router.post("/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    try:
        token_data = autenticar_usuario(db, credentials.correo, credentials.contraseña)
        return token_data
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="El Usuario no existe")

