from pydantic import BaseModel
from fastapi import FastAPI, Body, Query
from typing import Dict, Optional, List

"""
Execute app in console

uvicorn main:app --reload
uvicorn main:<<app_name>> --reload

View the documentation on the browser Swagger
http://127.0.0.1:8000/docs


View the documentation on the browser Redoc
http://127.0.0.1:8000/redoc

"""

# Init app
app: FastAPI = FastAPI()


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
