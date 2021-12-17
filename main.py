from fastapi import FastAPI
from typing import Dict

"""
Execute app in console

uvicorn main:app --reload
uvicorn main:<<app_name>> --reload

View the documentation on the browser Swagger
http://127.0.0.1:8000/docs

"""

# Init app
app: FastAPI = FastAPI()


# Path decoration operator
@app.get('/')
def home() -> Dict[str, str]:
    return {'greeting': 'HelloWorld!'}
