from distutils.log import debug
from fastapi import FastAPI
from fastapi.params import Query
import uvicorn
import argparse
import psycopg2

from controllers.ControllerRequests import ControllerRequests

from models.requests.RequestSaveResult import ResponseSaveResult
from models.requests.ResponseSaveResult import ResponseSaveResult

app = FastAPI()


@app.get("/test")
async def test_connection():
    try:
        print("beep")
        conn = psycopg2.connect()
    except Exception as e:
        print(e)


@app.post("/results", response_model=ResponseSaveResult)
async def post_results():
    try:
        ControllerRequests.save_result()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)
