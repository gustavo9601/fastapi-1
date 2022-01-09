from pydantic import BaseModel, Field, EmailStr, PaymentCardNumber, PositiveFloat
from fastapi import FastAPI, Body, Query, Path, Form, Header, Cookie, UploadFile, File, HTTPException
from typing import Dict, Optional, List
from enum import Enum
import shutil

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
    password: str = Field(..., min_length=2)


class User2(BaseModel):
    first_name = str
    last_name = str
    password: str = Field(..., min_length=2)


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='gus')
    password: str = Field(..., min_length=2, max_length=20, example='123')
    message: str = Field(default='Login successful', description='Message to return to the user')


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


@app.get('/players/details',
         tags=['Players'])
def show_players(
        first_name: Optional[str] = Query(None, min_length=1, max_length=10),
        age: int = Query(...)
) -> Dict[str, str]:
    return {
        'first_name': first_name,
        'age': age,
    }


# Request and Response Body
@app.post('/players',
          tags=['Players'])
# Body(...) // ... significa que el body request es obligatorio
def create_player(player: Player = Body(...)) -> Player:
    return player


@app.get('players_full/{player_id}',
         tags=['Players'])
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


# Se define que que atributos se deben excluir del return
@app.post('/create-user-2',
          response_model_exclude={'password'},
          status_code=200)  # Definiendo el tipo de code a retornar
def create_user(user: User2 = Body(...), ):
    return user


"""
Form => permite recibir datos desde un formulario hasta archivos
"""


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=200,
    response_model_exclude={'password'},
)
def login(username: str = Form(...), password=Form(...)):
    return LoginOut(username=username, password=password)


"""
Cookies and headers
"""


@app.post(path='/contact',
          status_code=200)
def contact(
        first_name: str = Form(..., max_length=20, min_length=1),
        last_name: str = Form(..., max_length=20, min_length=1),
        email: EmailStr = Form(...),
        message: str = Form(..., min_length=20),
        user_agent_header: Optional[str] = Header(default=None),
        cookie_ads: Optional[str] = Cookie(default=None)
):
    return {
        "status": "ok",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "message": message,
            "user_agent_header": user_agent_header,
            "cookie_ads": cookie_ads
        }
    }


"""
Uploading files


tags=['Uploads_files'] // permite agrupar los paths por tag
summary='Upload File (Image)' // titulo en la documentacion
"""


@app.post(path='/upload-file',
          summary='Upload File (Image)',
          tags=['Uploads_files'])
async def upload_file(
        image: UploadFile = File(...)
):
    """
    Upload File to server

    This path operation allow to upload any files into the server

    Parameters:
    - Request body parameter
        - **image: UploadFile** -> Binary File
    Returns:
    - Return dict with information of the file uploaded

    """
    with open('./files/' + image.filename, 'wb') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read()) / 1024, ndigits=2),  # Obtiene la cantidad de bytes
    }


@app.post(
    path='/upload-multiple-files',
    tags=['Uploads_files']
)
def upload_multiple_files(
        images: List[UploadFile] = File(...)
):
    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    } for image in images]

    return info_images


@app.get(path='/error-request/{age}')
def error_request(age: int):
    if (age < 18):
        raise HTTPException(
            status_code=500,
            detail='This person is less than 18 years old, you should be mayor'
        )
    return {
        "status": "ok"
    }


"""
deprecated=True // deja sin efecto un path, y lo muestra tachado en la documentacion
"""


@app.get('/path-deprecated', deprecated=True)
def deprecated_path():
    return {
        "data": False
    }
