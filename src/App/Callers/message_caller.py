from Callers.server_caller import ServerCaller

class MessageCaller(ServerCaller):
    def __init__(self):
        super().__init__()
        self.ext = "/message"
        
    def send(self, token, content):
        payload = {
            "token": token,
            "content": content
        }
        
        response = self.postRequest(payload)
        return response

    def getMessages(self, token):
        payload = {
            "token": token
        }

        response = self.getRequest(payload)
        return response.json()