import json
import uvicorn
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from fastapi import FastAPI, Body

app = FastAPI()
data_folder = './data/'

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


@app.post(
    path='/signup',
    response_model=User,
    response_model_exclude={'password'},
    status_code=201,
    tags=['Users'],
    summary='Register a User'  # Title in documentation
)
def signup(user: User = Body(...)):
    with open(f'{data_folder}users.json', 'r+', encoding='utf-8') as file:
        users = json.loads(file.read())  # parse string to json
        user_dict = user.dict()  # transform el request as a dict
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])

        # Add user to json
        users.append(user_dict)

        # Move top file
        file.seek(0)
        # Write into file the json
        file.write(json.dumps(users))

        return user


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
    with open(f'{data_folder}users.json', 'r', encoding='utf-8') as file:
        users = json.loads(file.read())  # parse string to json
        return users


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


"""
Tweets
"""


@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=200,
    tags=['Tweets'],
    summary='List all Tweets'
)
def home():
    with open(f'{data_folder}tweets.json', 'r', encoding='utf-8') as file:
        users = json.loads(file.read())  # parse string to json
        return users


@app.post(
    path='/tweets',
    response_model=Tweet,
    status_code=201,
    tags=['Tweets'],
    summary='Create Tweet'  # Title in documentation
)
def create_tweet(tweet: Tweet):
    with open(f'{data_folder}tweets.json', 'r+', encoding='utf-8') as file:
        tweets = json.loads(file.read())  # parse string to json
        tweet_dict = tweet.dict()  # transform the request as a dict
        print(tweet_dict)
        print(tweet_dict['by']['user_id'])
        print(tweet_dict['by']['birth_date'])
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict['updated_at'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])
        # Add tweet to json
        tweets.append(tweet_dict)
        # Move top file
        file.seek(0)
        # Write into file the json
        file.write(json.dumps(tweets))

        return tweet_dict


@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=200,
    tags=['Tweets'],
    summary='Show a Tweet'  # Title in documentation
)
def show_tweet(tweet_id: int):
    pass


@app.delete(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=200,
    tags=['Tweets'],
    summary='Delete a Tweet'  # Title in documentation
)
def delete_tweet(tweet_id: int):
    pass


@app.put(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=200,
    tags=['Tweets'],
    summary='Update a Tweet'  # Title in documentation
)
def update_tweet(tweet_id: int):
    pass


if __name__ == "__main__":
    uvicorn.run('app_1:app', host="localhost", port=8000, workers=2, reload=True)
