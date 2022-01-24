from distutils.log import debug
from fastapi import FastAPI
from fastapi.params import Query
import uvicorn
import psycopg2
from starlette.responses import Response

from controllers.ControllerRequests import ControllerRequests

from models.requests.RequestSaveResult import RequestSaveResult
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
async def post_results(points: int = Query(...), username: str = Query(...)):
    response = None
    try:
        response = ResponseSaveResult()
        response.is_success = True

        print("test")

    except Exception as e:
        print(e)
    # response: ResponseSaveResult = None
    # try:
    #     request_save_result = RequestSaveResult(points=points, username=username)
    #     print(request_save_result)
    #     response = await ControllerRequests.save_result(request_save_result)
    # except Exception as e:
    #     print(e)
    return response


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True, debug=True, workers=5)
