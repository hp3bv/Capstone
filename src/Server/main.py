from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from services.authentication.login_service import LoginService
from services.authentication.sign_up_service import SignUpService
from invokers.db.db_invoker import DBInvoker
from services.token.token_service import TokenService
from services.message.message_service import MessageService

app = FastAPI()
dbInvoker = DBInvoker()
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

class MessageRequest(BaseModel):
    token: str
    content: str

@app.post("/login")
def login(data: LoginRequest):
    result = loginService.login(data.key, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/signup")
def signup(data: SignUpRequest):
    result = signUpService.sign_up(data.email, data.username, data.password)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.post("/message")
def message(data: MessageRequest):
    result = messageService.publishMessage(data.token, data.content)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result