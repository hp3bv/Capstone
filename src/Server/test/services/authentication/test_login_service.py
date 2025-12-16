import pytest
from unittest.mock import Mock, patch
from src.Server.services.authentication.auth_service import AuthService
from src.Server.services.authentication.login_service import LoginService 

def createMockUser(username="testUser", password_hash="hashed_secret"):
    return {
        "username": username,
        "email": "test@test.com",
        "password_hash": password_hash,
        "attends_university": 1
    }

@patch('bcrypt.checkpw')
def test_checkPassword1(mock_checkpw):
    loginService = LoginService(Mock(), Mock())
    mock_checkpw.return_value = True
    
    result = loginService.checkPassword("password", "hash")
    
    assert result is True
    mock_checkpw.assert_called_once()

@patch('bcrypt.checkpw')
def test_checkPassword2(mock_checkpw):
    loginService = LoginService(Mock(), Mock())
    mock_checkpw.return_value = False
    
    assert loginService.checkPassword("wrong", "hash") is False

def test_loginWithEmail1():
    mockDB = Mock()
    mockDB.getUserFromEmail.return_value = None
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithEmail("test@test.com", "password")
    
    assert not response["success"]
    assert response["message"] == "Email does not exist"

@patch('bcrypt.checkpw')
def test_loginWithEmail2(mock_checkpw):
    mockDB = Mock()
    mockDB.getUserFromEmail.return_value = createMockUser()
    mock_checkpw.return_value = False
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithEmail("test@test.com", "wrongPassword")
    
    assert not response["success"]
    assert response["message"] == "Incorrect password"

@patch('bcrypt.checkpw')
def test_loginWithEmail3(mock_checkpw):
    mockDB = Mock()
    user = createMockUser()
    mockDB.getUserFromEmail.return_value = user
    mock_checkpw.return_value = True
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithEmail("test@test.com", "correctPassword")
    
    assert response["success"]
    assert response["user"] == user

def test_loginWithUsername1():
    mockDB = Mock()
    mockDB.getUserFromUsername.return_value = None
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithUsername("testUser", "password")
    
    assert not response["success"]
    assert response["message"] == "Username does not exist"

@patch('bcrypt.checkpw')
def test_loginWithUsername2(mock_checkpw):
    mockDB = Mock()
    mockDB.getUserFromUsername.return_value = createMockUser()
    mock_checkpw.return_value = False
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithUsername("testUser", "wrongPassword")
    
    assert not response["success"]
    assert response["message"] == "Incorrect password"

@patch('bcrypt.checkpw')
def test_loginWithUsername3(mock_checkpw):
    mockDB = Mock()
    user = createMockUser()
    mockDB.getUserFromUsername.return_value = user
    mock_checkpw.return_value = True
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.loginWithUsername("testUser", "correctPassword")
    
    assert response["success"]
    assert response["user"] == user

def test_login1():
    loginService = LoginService(Mock(), Mock())
    
    long_password = "a" * 25
    response = loginService.login("test@test.com", long_password)
    
    assert not response["success"]
    assert response["message"] == "Password is not valid"

def test_login2():
    loginService = LoginService(Mock(), Mock())
    
    response = loginService.login("!invalidKey", "validPassword")
    
    assert not response["success"]
    assert response["message"] == "Invalid email or username"

@patch('bcrypt.checkpw')
def test_login3(mock_checkpw):
    mockDB = Mock()
    mockDB.getUserFromEmail.return_value = createMockUser(username="emailUser")
    mock_checkpw.return_value = True
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.login("test@test.com", "validPassword")
    
    assert response["success"]
    assert response["message"] == "Successfully logged in"
    assert response["username"] == "emailUser"
    mockDB.getUserFromEmail.assert_called_once_with("test@test.com")

@patch('bcrypt.checkpw')
def test_login4(mock_checkpw):
    mockDB = Mock()
    mockDB.getUserFromUsername.return_value = createMockUser(username="standardUser")
    mock_checkpw.return_value = True
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.login("standardUser", "validPassword")
    
    assert response["success"]
    assert response["message"] == "Successfully logged in"
    assert response["username"] == "standardUser"
    mockDB.getUserFromUsername.assert_called_once_with("standardUser")

def test_login5():
    mockDB = Mock()
    mockDB.getUserFromUsername.return_value = None
    
    loginService = LoginService(mockDB, Mock())
    
    response = loginService.login("unknownUser", "validPassword")
    
    assert not response["success"]
    assert response["message"] == "Username does not exist"