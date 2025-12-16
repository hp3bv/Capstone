from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from src.Server.services.authentication.login_service import LoginService
from src.Server.services.authentication.sign_up_service import SignUpService
from src.Server.invokers.db.db_invoker import DBInvoker
from src.Server.services.token.token_service import TokenService
from src.Server.services.message.message_service import MessageService
from src.Server.services.university.group_service import GroupService
from src.Server.services.university.course_service import CourseService
from src.Server.services.university.university_service import UniversityService
from src.Server.data_format import *

dbPath = os.getenv("DB_PATH")
dbInvoker = DBInvoker(dbPath)

app = FastAPI()
dbInvoker = DBInvoker(dbPath)
tokenService = TokenService(dbInvoker)
loginService = LoginService(dbInvoker, tokenService)
signUpService = SignUpService(dbInvoker, tokenService)
messageService = MessageService(dbInvoker, tokenService)
groupService = GroupService(dbInvoker, tokenService)
courseService = CourseService(dbInvoker, tokenService)
universityService = UniversityService(dbInvoker, tokenService)

@app.post("/login")
def login(data: LoginRequest):
    result = loginService.login(data.key, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/sign_up")
def signup(data: SignUpRequest):
    result = signUpService.signUp(data.email, data.username, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/message")
def postMessage(data: MessagePostRequest):
    result = messageService.publishMessage(data.token, data.content, data.group_id)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/message")
def getMessage(data: MessageGetRequest):
    result = messageService.getMessages(data.token, data.group_id)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/groups_for_course")
def getGroupsForCourse(data: GroupsForCourse):
    result = groupService.getGroupsForCourse(data.token, data.cid)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/groups_for_user")
def getGroupsForCourse(data: GroupsForUser):
    result = groupService.getGroupsForUser(data.token)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/groups_for_course")
def getGroupsForCourse(data: GroupsForCourse):
    result = groupService.getGroupsForCourse(data.token, data.cid)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/join_group")
def joinGroup(data: GroupRequest):
    result = groupService.joinGroup(data.token, data.group_id)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/universities")
def searchUniversities(data: UniversityRequest):
    result = universityService.getUniversities(data.token)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/join_university")
def joinUniversity(data: UniversityJoinRequest):
    result = universityService.joinUniversiy(data.token, data.uid)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/course_lookup")
def lookupCourses(data: CourseLookupRequest):
    result = courseService.courseLookup(data.token, data.course_subj, data.course_no, data.course_name)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result