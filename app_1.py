import uvicorn
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Body

app = FastAPI()

"""
======================================
Models
======================================
"""


class User(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=3)
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    birth_date: Optional[date] = Field(default=None)


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., min_length=5, max_length=255, example='Hello Wold!')
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())
    by: User = Field(...)


"""
======================================
Routes
======================================
"""


@app.get("/", tags=['Home'])
def home():
    return {"Twitter API GM": "Hello World"}


@app.post(
    path='/signup',
    response_model=User,
    response_model_exclude={'password'},
    status_code=201,
    tags=['Users'],
    summary='Register a User'  # Title in documentation
)
def signup():
    pass


@app.post(
    path='/signup',
    response_model=User,
    response_model_exclude={'password'},
    status_code=201,
    tags=['Users'],
    summary='Register a User'  # Title in documentation
)
def signup():
    pass


@app.post(
    path='/login',
    response_model=User,
    response_model_exclude={'password'},
    status_code=200,
    tags=['Users'],
    summary='Login a user'  # Title in documentation
)
def login():
    pass


@app.get(
    path='/users',
    response_model=List[User],
    response_model_exclude={'password'},
    status_code=200,
    tags=['Users'],
    summary='List all Users'  # Title in documentation
)
def list_all_users():
    pass


@app.get(
    path='/users/{user_id}',
    response_model=User,
    response_model_exclude={'password'},
    status_code=200,
    tags=['Users'],
    summary='Get User'  # Title in documentation
)
def get_user(user_id: UUID):
    pass


@app.delete(
    path='/users/{user_id}',
    response_model=User,
    response_model_exclude={'password'},
    status_code=200,
    tags=['Users'],
    summary='Delete a user'  # Title in documentation
)
def delete_user(user_id: UUID):
    pass


@app.put(
    path='/users/{user_id}',
    response_model=User,
    response_model_exclude={'password'},
    status_code=200,
    tags=['Users'],
    summary='Update a user'  # Title in documentation
)
def update_user(user_id: UUID, user: User = Body(...)):
    pass


if __name__ == "__main__":
    uvicorn.run('app_1:app', host="localhost", port=8000, workers=2, reload=True)
