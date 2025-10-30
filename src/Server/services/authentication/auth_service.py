import bcrypt
import re

class AuthService:
    def __init__(self, dbInvoker, tokenServivces):
        self.dbInvoker = dbInvoker
        self.tokenServices = tokenServivces
    
    # Input validation
    def isValidEmail(self, email):
        return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email))
    
    def isValidUsername(self, user):
        return 3 <= len(user) <= 20 and user.isalnum()
    
    def isValidPassword(self, password):
        return 3 <= len(password) <= 20 and password.isalnum()
    
    # Password
    def hashPassword(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # Success message
    def success(self, username, message):
        token = self.tokenServices.createToken(username)
        return {"success": True, "message": message, "token": token}

    # Failure message
    def failure(self, message):
        return {"success": False, "message": message}
    
    # Retrieve user
    def retrieveUserFromUsername(self, username):
        return self.dbInvoker.getUserFromUsername(username)
    
    def retrieveUserFromEmail(self, email):
        return self.dbInvoker.getUserFromEmail(email)