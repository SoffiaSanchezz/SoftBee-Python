from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str = Field(..., min_length=6)
    direccion_apiario: str
    cantidad_colmenas: int
