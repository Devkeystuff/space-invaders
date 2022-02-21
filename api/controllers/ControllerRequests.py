from controllers.ControllerDatabase import ControllerDatabase

from models.requests.response_save_result import ResponseSaveResult
from models.requests.request_save_result import RequestSaveResult
from models.requests.response_get_all_results import ResponseGetAllResults


class ControllerRequests:
    @staticmethod
    #dabu visus rezultatus
    async def save_result(request: RequestSaveResult) -> ResponseSaveResult:
        #stradas sinhroni(vienlaikus) ar aplikaciju
        result = None
        try:
            result = ResponseSaveResult()

            result.result_id = await ControllerDatabase.save_result(request)
            if result.result_id:
                result.is_success = True
        except Exception as e:
            print(e, "ControllerRequests_submit_result")
        return result

    @staticmethod
    async def get_all_results() -> ResponseGetAllResults:
        result = None
        try:
            result = ResponseGetAllResults()

            result = await ControllerDatabase.get_all_results()
            result.is_success = True
        except Exception as e:
            print(e, "ControllerRequests_get_all_results")
        return result
