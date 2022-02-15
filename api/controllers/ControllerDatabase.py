from black import re
import psycopg2
from utils.DbCursor import DbCursor

from models.requests.request_save_result import RequestSaveResult

from models.requests.response_get_all_results import ResponseGetAllResults

from models.db.db_result import DbResult


class ControllerDatabase:
    @staticmethod
    async def save_result(result: RequestSaveResult) -> int:
        result_id = None
        try:
            cols = ["points", "username"]
            values = result.to_dict()

            with DbCursor() as cur:
                cur.execute(
                    f"""INSERT INTO results ({', '.join(cols)}) VALUES ({', '.join(["'%s'" % values[i] for i in cols])}) RETURNING result_id"""
                )
                (result_id,) = cur.fetchone()

        except Exception as e:
            print(e)
        return result_id

    @staticmethod
    async def get_all_results() -> ResponseGetAllResults:
        result = None
        try:
            with DbCursor() as cur:
                cur.execute(f"""SELECT * FROM results""")
                response = cur.fetchall()
                print(response)
        except Exception as e:
            print(e)

        return result
