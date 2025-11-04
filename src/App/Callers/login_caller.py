from .server_caller import ServerCaller

class LoginCaller(ServerCaller):
    def __init__(self):
        super().__init__()
        self.ext = "/login"
        
    def login(self, key, password):
        payload = {
            "key": key,
            "password": password
        }
        
        response = self.postRequest(payload)
        return response