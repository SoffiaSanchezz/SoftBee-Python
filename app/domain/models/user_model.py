from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from datetime import datetime
from app.infraestructure.database.base_class import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(TIMESTAMP, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_actualizacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    apiarios = relationship("Apiario", back_populates="usuario", cascade="all, delete-orphan")

class Apiario(Base):
    __tablename__ = "apiarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    cantidad_colmenas = Column(Integer, nullable=False)
    latitud = Column(String(20))
    longitud = Column(String(20))
    aplica_tratamientos = Column(Boolean, default=False)

    usuario = relationship("User", back_populates="apiarios")