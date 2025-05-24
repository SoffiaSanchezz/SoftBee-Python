
from pydantic import BaseModel, EmailStr, Field
from typing import List

class ApiarioCreate(BaseModel):
    direccion: str
    cantidad_colmenas: int

class UserCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str = Field(..., min_length=6)
    apiarios: List[ApiarioCreate]  # Ahora acepta una lista de apiarios

class UserLogin(BaseModel):
    correo: str
    contraseña: str