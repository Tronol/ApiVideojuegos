from pydantic import BaseModel

class VideojuegoBase(BaseModel):
    nombre: str
    imagen: str
    desarrollador: str
    descripcion: str
    plataforma: str
    clasificacion: str

class VideojuegoCreate(VideojuegoBase):
    pass

class VideojuegoResponse(VideojuegoBase):
    id: int

    class Config:
        from_attributes = True 

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class ListaDeDeseadosBase(BaseModel):
    usuario_id: int

class ListaDeDeseadosCreate(ListaDeDeseadosBase):
    videojuego_id: int

# Respuesta incluirá el videojuego completo
class ListaDeDeseadosResponse(ListaDeDeseadosBase):
    id: int
    videojuego: VideojuegoResponse  

    class Config:
        orm_mode = True