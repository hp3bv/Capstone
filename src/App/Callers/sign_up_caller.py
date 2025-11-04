from Callers.server_caller import ServerCaller

class SignUpCaller(ServerCaller):
    def __init__(self):
        super().__init__()
        self.ext = "/signup"
        
    def signUp(self, username, email, password):
        payload = {
            "email": email,
            "username": username,
            "password": password
        }
        
        response = self.postRequest(payload)
        return response