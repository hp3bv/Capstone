from datetime import datetime

class MessageService:
    def __init__(self, dbInvoker, tokenService):
        self.dbInvoker = dbInvoker
        self.tokenService = tokenService
    
    def publishMessage(self, token, content):
        tokenResponse = self.tokenService.validateToken(token)

        if not tokenResponse["valid"]:
            return self.failure(tokenResponse["message"])
        
        username = tokenResponse["username"]

        if len(content) > 1000:
            return self.failure("Message is too long")
        
        self.dbInvoker.addMessage(username, content)
        return self.success("Successfully published")
        
    def success(self, message):
        return {"success": True, "message": message}

    def failure(self, message):
        return {"success": False, "message": message}