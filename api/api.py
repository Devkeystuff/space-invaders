from fastapi import FastAPI
from fastapi.params import Query
import argparse


from models.requests.RequestUserRegister import RequestUserRegister 
from models.requests.ResponseUserRegister import ResponseUserRegister 

app = FastAPI()

@app.get('/users', response_model=ResponseUserRegister)
async def get_users(
    api_key: str = Query(...),
    email: str = Query(...)
) -> ResponseUserRegister:
    response: RequestUserRegister = None
    try:
        request_user_register = RequestUserRegister()
        request_user_register.api_key = api_key
        request_user_register.email = email

        response = await ControllerRequests.register_user()
    except Exception as e:
        print(e)
