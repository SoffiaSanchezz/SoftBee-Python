from sqlalchemy import Column, Integer, String
from app.infraestructure.database.base_class import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    direccion_apiario = Column(String, nullable=False)
    cantidad_colmenas = Column(Integer, nullable=False)
