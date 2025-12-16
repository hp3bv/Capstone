from src.Server.services.authentication.auth_service import AuthService
from src.Server.services.token.token_service import TokenService
from src.Server.invokers.db.db_invoker import DBInvoker

class SignUpService(AuthService):
    def __init__(self, dbInvoker: DBInvoker, tokenServices: TokenService):
        super().__init__(dbInvoker, tokenServices)

    def signUp(self, email, username, password):
        # Check if password is valid
        if not self.isValidPassword(password):
            return self.failure("Password is not valid")
        
        # Check if username is valid
        if not self.isValidUsername(username):
            return self.failure(f"Username, {username}, is not valid")
        
        # Check if email is valid
        if not self.isValidEmail(email):
            return self.failure("Email, {email}, is not valid")
        
        # Check if email is already taken
        user = self.retrieveUserFromEmail(email)
        if user:
            return self.failure("That email is taken")
        
        # Check if username is already taken
        user = self.retrieveUserFromUsername(username)
        if user:
            return self.failure("That username is already taken")
        
        self.createUser(email, username, password)

        return self.success(username, "Successfully signed up")

    def createUser(self, email, username, password):
        passwordHash = self.hashPassword(password)
        self.dbInvoker.addUser(username, email, passwordHash)