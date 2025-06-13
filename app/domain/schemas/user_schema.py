from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class ApiarioBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=255)
    cantidad_colmenas: int = Field(..., gt=0)
    latitud: Optional[str] = Field(None, max_length=20)
    longitud: Optional[str] = Field(None, max_length=20)
    aplica_tratamientos: bool = False

class ApiarioCreate(ApiarioBase):
    pass

class UserBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    telefono: str = Field(..., max_length=20)
    correo: EmailStr

class UserCreate(UserBase):
    contraseña: str = Field(..., min_length=8)
    apiarios: List[ApiarioCreate] = Field(..., min_items=1)

class UserResponse(UserBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True  # Cambiado de from_attributes a orm_mode para versiones anteriores

class UserLogin(BaseModel):
    correo: EmailStr
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ApiarioResponse(ApiarioBase):
    id: int
    usuario_id: int
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class PasswordResetRequest(BaseModel):
    correo: EmailStr

class PasswordReset(BaseModel):
    token: str
    nueva_contraseña: str = Field(..., min_length=8)

class PasswordResetResponse(BaseModel):
    message: str