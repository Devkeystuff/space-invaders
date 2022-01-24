from models.requests.RequestSaveResult import RequestUserRegister
from models.requests.ResponseSaveResult import ResponseUserRegister

from controllers.ControllerDatabase import ControllerDatabase


class ControllerRequests:
    @staticmethod
    def submit_result():
        try:
            ControllerDatabase.save_result()
        except Exception as e:
            print(e, "ControllerRequests_submit_result")
