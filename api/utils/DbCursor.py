import dotenv
import psycopg2
from dotenv import get_key, load_dotenv
import os

DB = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")


class DbCursor(object):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()
        self.conn = psycopg2.connect(
            f"dbname='{DB}' "
            f"host='localhost' "
            f"user='{USER}' "
            f"password='{PASS}'"
        )
        self.cursor = None

    def __enter__(self):
        self.conn.__enter__()
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.__exit__(self, exc_type, exc_val, exc_tb)
        self.conn.__exit__(exc_type, exc_val, exc_tb)
