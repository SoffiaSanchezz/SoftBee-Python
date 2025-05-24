from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.schemas.user_schema import UserCreate
from app.domain.services.user_service import crear_usuario
from app.infraestructure.database.session import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        nuevo_usuario = crear_usuario(db, user)
        return {"msg": "Usuario registrado exitosamente", "correo": nuevo_usuario.correo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
