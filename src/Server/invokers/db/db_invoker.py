import sqlite3
import os
from src.Server.invokers.db.sql_queries import Queries

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

    # Authentication
    def getUserFromEmail(self, email):
        self.cursor.execute(Queries.SELECT_EMAIL, {"email": email})
        return self.cursor.fetchone()

    def getUserFromUsername(self, username):
        self.cursor.execute(Queries.SELECT_USERNAME, {"username": username})
        return self.cursor.fetchone()

    def addUser(self, username, email, passwordHash):
        # FIX: Removed 'role_id' because your Schema's 'user' table doesn't have it.
        self.cursor.execute(
            Queries.ADD_USER,
            {
                "username": username, 
                "email": email, 
                "password_hash": passwordHash
                # "role_id": 1  <-- REMOVED
            }
        )
        self.conn.commit()

    # Messages
    def addMessage(self, username, content, group_id=1):
        self.cursor.execute(
            Queries.ADD_MESSAGE,
            {"username": username, "content": content, "group_id": group_id}
        )

        messageId = self.cursor.lastrowid
        self.conn.commit()
        return messageId

    def getMessages(self, groupId):
        self.cursor.execute(
            Queries.GET_MESSAGES,
            {"group_id": groupId}    
        )
        return self.cursor.fetchall()
    
    def getUniversities(self):
        self.cursor.execute(Queries.GET_UNIVERSITIES)
        return self.cursor.fetchall()
    
    def attends(self, username, uid):
        self.cursor.execute(
            Queries.ATTENDS_UNIVERSITY,
            {"username": username, "uid": uid}
        )
        self.conn.commit()
    
    def courseLookup(self, uid, courseSubj, courseNo, courseName):
        self.cursor.execute(
            Queries.COURSE_LOOKUP,
            {
                "uid": uid,
                "courseSubj": courseSubj,
                "courseNo": courseNo,
                "courseName": courseName
            }
        )
        return self.cursor.fetchall()
    
    def getGroupsForCourse(self, cid):
        self.cursor.execute(
            Queries.GET_GROUPS,
            {"cid": cid}
        )
        return self.cursor.fetchall()
    
    def getGroup(self, gid):
        self.cursor.execute(
            Queries.GET_GROUP,
            {"gid": gid}
        )
        return self.cursor.fetchone()
    
    def getGroupsForUser(self, username):
        self.cursor.execute(
            Queries.GET_GROUPS_FOR_USER,
            {"username": username}
        )
        return self.cursor.fetchall()
    
    def joinGroup(self, gid, username):
        self.cursor.execute(
            Queries.JOIN_GROUP,
            {"username": username, "gid": gid}
        )
        self.conn.commit()