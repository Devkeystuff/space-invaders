from controllers.ControllerDatabase import ControllerDatabase


from models.requests.ResponseSaveResult import ResponseSaveResult


class ControllerRequests:
    @staticmethod
    async def submit_result() -> ResponseSaveResult:
        try:
            await ControllerDatabase.save_result()
        except Exception as e:
            print(e, "ControllerRequests_submit_result")
