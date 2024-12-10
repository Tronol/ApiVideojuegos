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

class ListaDeDeseadosBase(BaseModel):
    videojuego_id: int
    usuario_id: int 

class ListaDeDeseadosCreate(ListaDeDeseadosBase):
    pass

class ListaDeDeseadosResponse(ListaDeDeseadosBase):
    id: int

    class Config:
        orm_mode = True