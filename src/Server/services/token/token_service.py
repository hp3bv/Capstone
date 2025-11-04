from jose import jwt, JWTError
from dotenv import load_dotenv
import os

KEY = os.environ.get("KEY")
if not KEY:
    raise ValueError("KEY not set")

ALGORITHM = "HS256"

class TokenService:
    def __init__(self, dbInvoker):
        self.dbInvoker = dbInvoker

    # Token creation
    def createToken(self, username):
        payload = {"sub": username}
        token = jwt.encode(payload, KEY, algorithm=ALGORITHM)
        return token
    
    def validateToken(self, token):
        try:
            payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                return {"valid": False, "message": "Token is invalid or expired"}
            
            # Ensure user is in database
            user = self.dbInvoker.getUserFromUsername(username)
            if not user:
                return {"valid": False, "message": "User not found"}
            
            return {"valid": True, "username": username}
        except JWTError:
            return {"valid": False, "message": "Token is invalid or expired"}