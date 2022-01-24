import psycopg2


class ControllerDatabase:
    @staticmethod
    async def save_result():
        conn = psycopg2.connect()
        # with DbCursor as cursor:
        # cursor
        print("saved")
