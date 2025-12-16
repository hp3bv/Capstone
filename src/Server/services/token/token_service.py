from src.Server.invokers.db.db_invoker import DBInvoker

from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = "HS256"

class TokenService:
    def __init__(self, dbInvoker: DBInvoker):
        self.dbInvoker = dbInvoker
        self.secretKey = os.environ.get("KEY")
        if not self.secretKey:
            raise ValueError("KEY not set")

    # Token creation
    def createToken(self, username):
        payload = {"sub": username}
        token = jwt.encode(payload, self.secretKey, algorithm=ALGORITHM)
        return token
    
    def validateToken(self, token):
        try:
            payload = jwt.decode(token, self.secretKey, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                return {"valid": False, "message": "Token is invalid or expired"}
            
            # Ensure user is in database
            user = self.dbInvoker.getUserFromUsername(username)
            if not user:
                return {"valid": False, "message": "User not found"}
            
            return {"valid": True, "user": user}
        except JWTError:
            return {"valid": False, "message": "Token is invalid or expired"}