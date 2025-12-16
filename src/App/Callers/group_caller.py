from Callers.server_caller import ServerCaller

class GroupCaller(ServerCaller):
    def __init__(self):
        super().__init__()
        self.ext = "/groups"
        
    def getGroupsForUser(self, token):
        payload = {
            "token": token
        }
        
        response = self.getRequest(payload, "_for_user")
        return response.json()
    
    def getJoinableGroups(self, token):
        payload = {
            "token": token
        }
        
        response = self.getRequest(payload, "_joinable")
        return response.json()
    
    