from pydantic import BaseModel

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
    group_id: int

class MessageGetRequest(BaseModel):
    token: str
    group_id: int
    
class GroupRequest(BaseModel):
    token: str
    group_id: int
    
class GroupsForCourse(BaseModel):
    token: str
    cid: int
    
class GroupsForUser(BaseModel):
    token: str
    
class UniversityRequest(BaseModel):
    token: str
    
class UniversityJoinRequest(BaseModel):
    token: str
    uid: int

class CourseLookupRequest(BaseModel):
    token: str
    course_no: str
    course_subj: str
    course_name: str