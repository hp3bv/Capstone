from services.authentication.auth_service import AuthService

class SignUpService(AuthService):
    def __init__(self, dbInvoker, tokenServices):
        super().__init__(dbInvoker, tokenServices)

    def sign_up(self, email, username, password):
        # Check if password is valid
        if not self.isValidPassword(password):
            return self.failure("Password is not valid")
        
        # Check if username is valid
        if not self.isValidUsername(username):
            return self.failure("Username is not valid")
        
        # Check if email is valid
        if not self.isValidEmail(email):
            return self.failure("Email is not valid")
        
        # Check if email is already taken
        user = self.retrieveUserFromEmail(email)
        if user:
            return self.failure("That email is taken")
        
        # Check if username is already taken
        user = self.retrieveUserFromUsername(username)
        if user:
            return self.failure("That username is already taken")
        
        self.create_user(email, username, password)

        return self.success(username, "Successfully signed up")

    def create_user(self, email, username, password):
        passwordHash = self.hashPassword(password)
        self.dbInvoker.addUser(username, email, passwordHash)