from sqlalchemy.orm import Session
from models import Videojuego
from schemas import VideojuegoCreate

# Crear un videojuego
def create_videojuego(videojuego: VideojuegoCreate, db: Session):
    db_videojuego = Videojuego(**videojuego.dict())
    db.add(db_videojuego)
    db.commit()
    db.refresh(db_videojuego)
    return db_videojuego

# Obtener todos los videojuegos
def get_videojuegos(db: Session):
    return db.query(Videojuego).all()
