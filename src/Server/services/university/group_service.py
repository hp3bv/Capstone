from src.Server.services.token.token_service import TokenService
from src.Server.invokers.db.db_invoker import DBInvoker

class GroupService:
    def __init__(self, dbInvoker: DBInvoker, tokenService: TokenService):
        self.dbInvoker = dbInvoker
        self.tokenService = tokenService
        
    def getGroupsForCourse(self, token, cid):
        response = self.tokenService.validateToken(token)
        
        if not response["valid"]:
            return {"success": False, "message": response["message"]}
        
        groups = self.dbInvoker.getGroupsForCourse(cid)
        return {"success": True, "groups": groups}
    
    def getGroupsForUser(self, token):
        response = self.tokenService.validateToken(token)
        
        if not response["valid"]:
            return {"success": False, "message": response["message"]}
        
        user = response["user"]
        
        groups = self.dbInvoker.getGroupsForUser(user["username"])
        
        return {"success": True, "data": groups}
    
    def joinGroup(self, token, gid):
        response = self.tokenService.validateToken(token)
        
        if not response["valid"]:
            return {"success": False, "message": response["message"]}
        
        user = response["user"]
        
        isGroupFullResponse = self.isGroupFull(gid)
        
        if not isGroupFullResponse["success"]:
            return isGroupFullResponse
        
        if isGroupFullResponse["isFull"]:
            return {"success": False, "message": "Group is full"}
    
        self.dbInvoker.joinGroup(gid, user["username"])
        
        return {"success": True}
        
    def isGroupFull(self, gid):
        response = self.dbInvoker.getGroup(gid)
        
        if not response:
            return {"success": False, "message": "Group does not exist"}
        
        if response["max_size"] <= response["total_users"]: 
            return {"success": True, "isFull": True}
        
        return {"success": True, "isFull": False}