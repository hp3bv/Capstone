from src.Server.services.token.token_service import TokenService
from src.Server.invokers.db.db_invoker import DBInvoker

class CourseService:
    def __init__(self, dbInvoker: DBInvoker, tokenService: TokenService):
        self.dbInvoker = dbInvoker
        self.tokenService = tokenService
        
    def courseLookup(self, token, courseSubj, courseNo, courseName):
        tokenResponse = self.tokenService.validateToken(token)
        
        if not tokenResponse["valid"]:
            return {"success": False, "message": tokenResponse["message"]}
        
        user = tokenResponse["user"]
                
        courses = self.dbInvoker.courseLookup(user["attends_university"], courseSubj, courseNo, courseName)
        return {"success": True, "courses": courses}