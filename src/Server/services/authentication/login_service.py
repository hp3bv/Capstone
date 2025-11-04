from services.authentication.auth_service import AuthService
import bcrypt

class LoginService(AuthService):
    def __init__(self, dbInvoker, tokenServices):
        super().__init__(dbInvoker, tokenServices)

    def login(self, key, password):
        if not self.isValidPassword(password):
            return self.failure("Password is not valid")
        
        if self.isValidEmail(key):
            response = self.loginWithEmail(key, password)
        elif self.isValidUsername(key):
            response = self.loginWithUsername(key, password)
        else:
            return self.failure("Invalid email or username")
        
        if response["success"]:
            return self.success(response["user"]["username"], "Successfully logged in")
        else:
            return response


    def loginWithEmail(self, email, password):
        user = self.retrieveUserFromEmail(email)
        
        if not user:
            return self.failure("Email does not exist")
        
        if not self.checkPassword(password, user["password_hash"]):
            return self.failure("Incorrect password")
        
        return {"success": True, "user": user}
        
    def loginWithUsername(self, username, password):
        user = self.retrieveUserFromUsername(username)

        if not user:
            return self.failure("Username does not exist")
        
        if not self.checkPassword(password, user["password_hash"]):
            return self.failure("Incorrect password")
        
        return {"success": True, "user": user}

    def checkPassword(self, password, hashed):
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))