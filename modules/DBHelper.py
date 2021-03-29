import sqlite3
from sqlite3 import Error

class DBHelper:
    def create_db_connection(self, db_path: str):
        # conn = sqlite3.connect(os.path.sep.join(['db', 'saqer.db']))
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        return conn
