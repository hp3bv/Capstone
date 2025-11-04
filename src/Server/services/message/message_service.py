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
        
        messageId = self.dbInvoker.addMessage(username, content)
        return self.successfullyPosted(messageId)
    
    def getMessages(self, token):
        tokenResponse = self.tokenService.validateToken(token)

        if not tokenResponse["valid"]:
            return self.failure(tokenResponse["message"])
        
        messages = self.dbInvoker.getMessages()
        return self.successfulyRetreived(messages)
        
    def successfullyPosted(self, messageId):
        return {"success": True, "message": "Successfully published", "messageId": messageId}
    
    def successfulyRetreived(self, messages):
        return {"success": True, "messages": messages}

    def failure(self, message):
        return {"success": False, "message": message}