from Callers.server_caller import ServerCaller

class MessageCaller(ServerCaller):
    def __init__(self):
        super().__init__()
        self.ext = "/message"
        
    def send(self, token, groupId, content):
        payload = {
            "token": token,
            "group_id": groupId,
            "content": content
        }
        
        response = self.postRequest(payload)
        return response

    def getMessages(self, token, groupId):
        payload = {
            "token": token,
            "group_id": groupId
        }

        response = self.getRequest(payload)
        return response.json()