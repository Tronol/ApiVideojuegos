from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

# Modelo de lista de deseados
class ListaDeDeseados(Base):
    __tablename__ = "lista_de_deseados"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    videojuego_id = Column(Integer, ForeignKey("videojuegos.id"), nullable=False)

    usuario = relationship("User", back_populates="listas_de_deseados")
    videojuego = relationship("Videojuego")

# Modelo de usuario
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    listas_de_deseados = relationship("ListaDeDeseados", back_populates="usuario")

# Modelo de videojuego
class Videojuego(Base):
    __tablename__ = "videojuegos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    imagen = Column(String, nullable=False)
    desarrollador = Column(String, nullable=False)
    descripcion = Column(String, nullable= False)
    plataforma = Column(String, nullable=False)
    clasificacion = Column(String, nullable=False)
    
