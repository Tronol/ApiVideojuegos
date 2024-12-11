from sqlalchemy.orm import Session
from models import Videojuego, ListaDeDeseados
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

def agregar_a_lista(usuario_id: int, videojuego_id: int, db: Session):
    entrada_existente = db.query(ListaDeDeseados).filter(
        ListaDeDeseados.usuario_id == usuario_id,
        ListaDeDeseados.videojuego_id == videojuego_id,
    ).first()

    if entrada_existente:
        return entrada_existente  # El videojuego ya está en la lista

    nueva_entrada = ListaDeDeseados(usuario_id=usuario_id, videojuego_id=videojuego_id)
    db.add(nueva_entrada)
    db.commit()
    db.refresh(nueva_entrada)
    return nueva_entrada

def obtener_lista(usuario_id: int, db: Session):
    resultados = (
        db.query(ListaDeDeseados)
        .join(Videojuego, ListaDeDeseados.videojuego_id == Videojuego.id)
        .filter(ListaDeDeseados.usuario_id == usuario_id)
        .all()
    )
    return resultados


