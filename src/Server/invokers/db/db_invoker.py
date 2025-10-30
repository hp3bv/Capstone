import sqlite3
from invokers.db.sql_queries import Queries

class DBInvoker:
    def __init__(self, db_path="group_management.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # lets you access columns by name
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def getUserFromEmail(self, email):
        self.cursor.execute(Queries.SELECT_EMAIL, {"email": email})
        return self.cursor.fetchone()

    def getUserFromUsername(self, username):
        self.cursor.execute(Queries.SELECT_USERNAME, {"username": username})
        return self.cursor.fetchone()

    def addUser(self, username, email, password_hash):
        self.cursor.execute(
            Queries.ADD_USER,
            {
                "username": username, 
                "email": email, 
                "password_hash": password_hash, 
                "role_id": 1
            }
        )
        self.conn.commit()

    def addMessage(self, username, content, group_id=1):
        self.cursor.execute(
            Queries.ADD_MESSAGE,
            {"username": username, "content": content, "group_id": group_id}
        )
        self.conn.commit()
