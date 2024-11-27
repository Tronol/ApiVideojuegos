from sqlalchemy import Column, Integer, String
from database import Base

# Modelo de usuario
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Modelo de videojuego
class Videojuego(Base):
    __tablename__ = "videojuegos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    imagen = Column(String, nullable=False)
    desarrollador = Column(String, nullable=False)
    plataforma = Column(String, nullable=False)
    clasificacion = Column(String, nullable=False)
