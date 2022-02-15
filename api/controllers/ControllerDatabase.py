from black import re
import psycopg2
from utils.DbCursor import DbCursor

from models.requests.request_save_result import RequestSaveResult

from models.requests.response_get_all_results import ResponseGetAllResults

from models.db.db_result import DbResult
#RequestSaveResult datu tips lai saprastu kadaa formaa dati tiek izmantoti serveriiiiiiiiiiiii


#class- nosaka db strukturu. class var saturt vairakus mainigus
class ControllerDatabase:
    # statiska metode, kura pienem rezultatu db
    @staticmethod
    async def save_result(result: RequestSaveResult) -> int:
        result_id = None
        try:
            cols = ["points", "username"]
            # mainigais
            values = result.to_dict()

            with DbCursor() as cur:
                # cur palidz komunicet ar db
                # izsauca darbibas ar db
                cur.execute(
                    f"""INSERT INTO results ({', '.join(cols)}) VALUES ({', '.join(["'%s'" % values[i] for i in cols])}) RETURNING result_id"""
                )
                #
                (result_id,) = cur.fetchone()
                # python tuple, lidzigi kaa list, bet ar apalam iekavam 
                # tuple datus nevar mainit, lista var mainit
                # ()
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
