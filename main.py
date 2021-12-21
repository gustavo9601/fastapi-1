from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber, PositiveFloat
from fastapi import FastAPI, Body, Query, Path
from typing import Dict, Optional, List
from enum import Enum

"""
Execute app in console

uvicorn main:app --reload
uvicorn main:<<app_name>> --reload

View the documentation on the browser Swagger
http://127.0.0.1:8000/docs


View the documentation on the browser Redoc
http://127.0.0.1:8000/redoc

"""

"""
Tipos de datos espciales pydantic

https://pydantic-docs.helpmanual.io/usage/types/#urls
"""

# Init app
app: FastAPI = FastAPI()


# Enums
class HairColor(Enum):
    white: str = 'white'
    black: str = 'black'
    brown: str = 'brown'
    red: str = 'red'
    blonde: str = 'blonde'
    tinted: str = 'tinted'


# Models
class Player(BaseModel):
    """
    Definiiendo atributos
    """
    first_name = str
    last_name = str
    age: int
    is_active: bool
    # Se usa optional permite que no sea obligatorio definir el campo, y le asginamos un valor por default
    hair_color: Optional[str] = None

    # Permite definir algunos ejemplos de pruebas para el api
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Gustavo",
                "last_name": "Marquez",
                "age": 25,
                "is_active": True,
                "hair_color": ""
            }
        }


class Location(BaseModel):
    # Verificacion propia sobre el modelo
    #    example='Bogota' // Permite generar un valor por default para la documentacion del api
    city: str = Field(
        ...,
        title='Ciudad',
        min_length=1,
        max_length=50,
        example='Bogota'
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Cundinamarca'
    )
    age: int = Field(
        ...,
        gt=0,
        le=100,
        example=25
    )
    # Asegura que los valores seran los definidos en el enum
    hair_color: Optional[HairColor] = Field(default=None)


class User(BaseModel):
    weight: Optional[PositiveFloat] = Field(default=None)
    email: EmailStr = Field(
        ...,
        title="Person Email")
    card: PaymentCardNumber = Field(
        ...,
        title="Payment Card")


# Path decoration operator
@app.get('/')
def home() -> Dict[str, str]:
    return {'greeting': 'HelloWorld!'}


# Path parameter
@app.get('/users/{user_id}')
def home(user_id: int) -> Dict[str, int]:
    return {'user_id': user_id}


# Query Params
# Query => ? & // Tambien se pasan las validaciones
# Query(...)  // Hace obligatorio el param
"""
Otras validaciones Query
ge => greater or equal than
le => less or equal than
gt => greater than
lt => less than

Agregando descripcion al parametro para la documentation
Query(
	None, 
	title="ID del usuario", 
	description="El ID se consigue entrando a las configuraciones del perfil");

"""


@app.get('/players/details')
def show_players(
        first_name: Optional[str] = Query(None, min_length=1, max_length=10),
        age: int = Query(...)
) -> Dict[str, str]:
    return {
        'first_name': first_name,
        'age': age,
    }


# Request and Response Body
@app.post('/players')
# Body(...) // ... significa que el body request es obligatorio
def create_player(player: Player = Body(...)) -> Player:
    return player


@app.get('players_full/{player_id}')
# gt = 0 // greater than 0
def get_players_full(player_id: int = Path(..., gt=0, title='ID player', description='Id player en entero')):
    return {
        player_id: player_id
    }


@app.put('/validation_params_body')
def validation_params_body(person_id: int = Path(..., title='Id Body'),
                           player: Player = Body(...),
                           location: Location = Body(...)
                           ):
    # .dict() // convierte a dict
    results = player.dict()
    # Unimos los diccionarios
    results.update(location.dict())
    return results
