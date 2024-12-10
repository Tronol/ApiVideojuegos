from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from database import Base, engine, get_db
from crud import create_videojuego, get_videojuegos, agregar_a_lista, obtener_lista
from schemas import Token, VideojuegoCreate, VideojuegoResponse, UserCreate, UserResponse, ListaDeDeseadosResponse, ListaDeDeseadosCreate
from models import User, Videojuego
from typing import List

# Inicializar la aplicación
app = FastAPI(
    title="API de Videojuegos",
    description="Una API para gestionar videojuegos, usuarios y listas de deseados.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Login", "description": "Rutas relacionadas con el registro e inicio de sesión."},
        {"name": "Videojuegos", "description": "Rutas para gestionar videojuegos."},
        {"name": "Deseados", "description": "Rutas para gestionar las listas de deseados de los usuarios."},
    ],
)
# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Ruta para registrar usuarios
@app.post("/register/", response_model=UserResponse, tags=["Login"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Ruta para iniciar sesión
@app.post("/login/", response_model=Token, tags=["Login"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
# Ruta para crear videojuegos (requiere autenticación)
@app.post("/videojuegos/", response_model=VideojuegoResponse, tags=["Videojuegos"])
def create_videojuego_endpoint(
    videojuego: VideojuegoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_videojuego(videojuego, db)

@app.get("/videojuegos/", response_model=list[VideojuegoResponse], tags=["Videojuegos"])
def list_videojuegos(db: Session = Depends(get_db)):
    return get_videojuegos(db)

@app.get("/videojuegos/{id}", response_model=VideojuegoResponse, tags=["Videojuegos"])
def get_videojuego_by_id(id: int, db: Session = Depends(get_db)):
    videojuego = db.query(Videojuego).filter(Videojuego.id == id).first()
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return videojuego

@app.get("/videojuegos/desarrollador/{desarrollador}", response_model=List[VideojuegoResponse], tags=["Videojuegos"])
def get_videojuegos_by_desarrollador(desarollador: str, db: Session = Depends(get_db)):
    videojuegos = db.query(Videojuego).filter(Videojuego.desarrollador == desarollador).all()
    if not videojuegos:
        raise HTTPException(status_code=404, detail="No se encontraron videojuegos para el desarrollador especificado")
    return videojuegos

@app.get("/videojuegos/clasificacion/{clasificacion}", response_model=List[VideojuegoResponse], tags=["Videojuegos"])
def get_videojuegos_by_clasificacion(clasificacion: str, db: Session = Depends(get_db)):
    videojuegos = db.query(Videojuego).filter(Videojuego.clasificacion == clasificacion).all()
    if not videojuegos:
        raise HTTPException(status_code=404, detail="No se encontraron videojuegos para la clasificación especificada")
    return videojuegos




@app.post("/lista_de_deseados/", response_model=ListaDeDeseadosResponse, tags=["Deseados"])
def agregar_a_lista_endpoint(
    lista_data: ListaDeDeseadosCreate,  # Usa el esquema de entrada
    db: Session = Depends(get_db),
):
    return agregar_a_lista(lista_data.usuario_id, lista_data.videojuego_id, db)


@app.get("/lista_de_deseados/{usuario_id}", response_model=List[ListaDeDeseadosResponse], tags=["Deseados"])
def obtener_lista_por_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    lista = obtener_lista(usuario_id, db)
    if not lista:
        raise HTTPException(status_code=404, detail="No se encontró una lista para este usuario.")
    return lista
