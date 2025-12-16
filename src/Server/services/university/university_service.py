from src.Server.services.token.token_service import TokenService
from src.Server.invokers.db.db_invoker import DBInvoker

class UniversityService:
    def __init__(self, dbInvoker: DBInvoker, tokenService: TokenService):
        self.dbInvoker = dbInvoker
        self.tokenService = tokenService
        
    def getUniversities(self, token):
        tokenResponse = self.tokenService.validateToken(token)
        
        if not tokenResponse["valid"]:
            return {"success": False, "message": tokenResponse["message"]}
        
        universities = self.dbInvoker.getUniversities()
        return {"success": True, "universities": universities}
    
    def joinUniversiy(self, token, uid):
        tokenResponse = self.tokenService.validateToken(token)
        
        if not tokenResponse["valid"]:
            return {"success": False, "message": tokenResponse["message"]}
        
        user = tokenResponse["user"]
        
        self.dbInvoker.attends(user["username"], uid)
        return {"success": True}