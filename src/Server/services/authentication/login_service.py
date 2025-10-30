from services.authentication.auth_service import AuthService
import bcrypt

class LoginService(AuthService):
    def __init__(self, dbInvoker, tokenServices):
        super().__init__(dbInvoker, tokenServices)

    def login(self, key, password):
        if not self.isValidPassword(password):
            return self.failure("Password is not valid")
        
        if self.isValidEmail(key):
            user = self.loginWithEmail(key, password)
            return self.success(user["username"], "Successfully logged in")
        elif self.isValidUsername(key):
            user = self.loginWithUsername(key, password)
            return self.success(user["username"], "Successfully logged in")
        else:
            self.failure("Invalid email or username")

    def loginWithEmail(self, email, password):
        user = self.retrieveUserFromEmail(email)
        
        if not user:
            return self.failure("Email does not exist")
        
        if not self.checkPassword(password, user["PasswordHash"]):
            return self.failure("Incorrect password")
        
        return user
        
    def loginWithUsername(self, username, password):
        user = self.retrieveUserFromUsername(username)

        if not user:
            return self.failure("Username does not exist")
        
        if not self.checkPassword(password, user["password_hash"]):
            return self.failure("Incorrect password")
        
        return user

    def checkPassword(self, password, hashed):
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))