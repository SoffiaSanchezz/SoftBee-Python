from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infraestructure.database.base_class import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)

    apiarios = relationship("Apiario", back_populates="usuario", cascade="all, delete-orphan")

class Apiario(Base):
    __tablename__ = "apiarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    direccion = Column(String, nullable=False)
    cantidad_colmenas = Column(Integer, nullable=False)

    usuario = relationship("User", back_populates="apiarios")
