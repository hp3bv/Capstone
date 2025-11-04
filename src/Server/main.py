from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from src.Server.services.authentication.login_service import LoginService
from src.Server.services.authentication.sign_up_service import SignUpService
from src.Server.invokers.db.db_invoker import DBInvoker
from src.Server.services.token.token_service import TokenService
from src.Server.services.message.message_service import MessageService

dbPath = os.getenv("DB_PATH", "group_management.db")
dbInvoker = DBInvoker(dbPath)

app = FastAPI()
dbInvoker = DBInvoker(dbPath)
tokenService = TokenService(dbInvoker)
loginService = LoginService(dbInvoker, tokenService)
signUpService = SignUpService(dbInvoker, tokenService)
messageService = MessageService(dbInvoker, tokenService)
# Define how to expect data
class LoginRequest(BaseModel):
    key: str
    password: str

class SignUpRequest(BaseModel):
    email: str
    username: str
    password: str

class MessagePostRequest(BaseModel):
    token: str
    content: str

class MessageGetRequest(BaseModel):
    token: str

@app.post("/login")
def login(data: LoginRequest):
    result = loginService.login(data.key, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/signup")
def signup(data: SignUpRequest):
    result = signUpService.signUp(data.email, data.username, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/message")
def postMessage(data: MessagePostRequest):
    result = messageService.publishMessage(data.token, data.content)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/message")
def getMessage(data: MessageGetRequest):
    result = messageService.getMessages(data.token)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result