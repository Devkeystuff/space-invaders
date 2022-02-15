from distutils.log import debug
from fastapi import FastAPI
from fastapi.params import Query
import uvicorn
import psycopg2
from starlette.responses import Response


from controllers.ControllerRequests import ControllerRequests

from models.requests.request_save_result import RequestSaveResult
from models.requests.response_save_result import ResponseSaveResult
from models.requests.response_get_all_results import ResponseGetAllResults
from models.requests.request_get_all_results import RequestGetAllResults

app = FastAPI()


@app.get("/test")
async def test_connection():
    try:
        print("beep")

    except Exception as e:
        print(e)


@app.post("/results", response_model=ResponseSaveResult)
async def post_results(points: int = Query(...), username: str = Query(...)):
    response = ResponseSaveResult()
    try:
        request_save_result = RequestSaveResult(points=points, username=username)
        response = await ControllerRequests.save_result(request_save_result)
    except Exception as e:
        print(e)
    return response


@app.get("/results", response_model=ResponseGetAllResults)
async def get_results():
    response = ResponseGetAllResults()
    try:
        response.results = await ControllerRequests.get_all_results()
    except Exception as e:
        print(e)
    return response


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True, debug=True, workers=5)
