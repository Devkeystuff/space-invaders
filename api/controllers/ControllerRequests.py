from models.requests.RequestUserRegister import RequestUserRegister
from models.requests.ResponseUserRegister import ResponseUserRegister

class ControllerRequests:
    @staticmethod
    def register_user(request: RequestUserRegister) -> ResponseUserRegister:
        response: ResponseUserRegister = None
        try:
            if ControllerRequests.validate_request(request, response):
                print("")
            else:
                response.error_code = ErrorCode.incorrect_key
        except Exception as e:
            print(e)