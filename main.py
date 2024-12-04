from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from database import Base, engine, get_db
from crud import create_videojuego, get_videojuegos
from schemas import Token, VideojuegoCreate, VideojuegoResponse, UserCreate, UserResponse
from models import User, Videojuego

# Inicializar la aplicación
app = FastAPI()

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Ruta para registrar usuarios
@app.post("/register/", response_model=UserResponse)
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
@app.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para obtener videojuegos (sin autenticación)
@app.get("/videojuegos/", response_model=list[VideojuegoResponse])
def list_videojuegos(db: Session = Depends(get_db)):
    return get_videojuegos(db)

@app.get("/videojuegos/{id}", response_model=VideojuegoResponse)
def get_videojuego_by_id(id: int, db: Session = Depends(get_db)):
    videojuego = db.query(Videojuego).filter(Videojuego.id == id).first()
    if not videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return videojuego

# Ruta para crear videojuegos (requiere autenticación)
@app.post("/videojuegos/", response_model=VideojuegoResponse)
def create_videojuego_endpoint(
    videojuego: VideojuegoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_videojuego(videojuego, db)
