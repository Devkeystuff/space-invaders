import psycopg2
from utils.DbCursor import DbCursor

from models.requests.RequestSaveResult import RequestSaveResult

from models.db.db_results import DbResults


class ControllerDatabase: 
    # statiska metode, kura pienem rezultatu db
    @staticmethod
    async def save_result(result: RequestSaveResult) -> int:     
        try:
            cols = ["points", "username"]
            # mainigais

            print(result)

            with DbCursor() as cur:
                #cur palidz komunicet ar db
                # izsauca darbibas ar db
                cur.execute(
                    """INSERT INTO results ({', '.join(cols)}) VALUES (12, 'test') RETURNING result_id"""
                )
                rows = cur.fetchone()
                print(rows)

        except Exception as e:
            print(e)
