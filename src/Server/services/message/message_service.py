from src.Server.services.token.token_service import TokenService
from src.Server.invokers.db.db_invoker import DBInvoker

from datetime import datetime

class MessageService:
    def __init__(self, dbInvoker: DBInvoker, tokenService: TokenService):
        self.dbInvoker = dbInvoker
        self.tokenService = tokenService
    
    def publishMessage(self, token, content, groupId):
        tokenResponse = self.tokenService.validateToken(token)

        if not tokenResponse["valid"]:
            return self.failure(tokenResponse["message"])
        
        user = tokenResponse["user"]

        if len(content) > 1000:
            return self.failure("Message is too long")
        
        if not self.groupExists(groupId):
            return self.failure("Group does not exist")
        
        messageId = self.dbInvoker.addMessage(user["username"], content, groupId)
        return self.successfullyPosted(messageId)
    
    def getMessages(self, token, groupId):
        tokenResponse = self.tokenService.validateToken(token)

        if not tokenResponse["valid"]:
            return self.failure(tokenResponse["message"])
        
        if not self.groupExists(groupId):
            return self.failure("Group does not exist")
        
        messages = self.dbInvoker.getMessages(groupId)
        return self.successfulyRetreived(messages)
    
    def groupExists(self, groupId):
        response = self.dbInvoker.getGroup(groupId)
        return response is not None
        
    def successfullyPosted(self, messageId):
        return {"success": True, "message": "Successfully published", "messageId": messageId}
    
    def successfulyRetreived(self, messages):
        return {"success": True, "messages": messages}

    def failure(self, message):
        return {"success": False, "message": message}