import pytest
from unittest.mock import Mock, patch
from src.Server.services.authentication.sign_up_service import SignUpService

def get_service_and_mocks():
    mockDB = Mock()
    mockToken = Mock()
    service = SignUpService(mockDB, mockToken)
    return service, mockDB, mockToken

def test_signUp1():
    service, mockDB, _ = get_service_and_mocks()
    
    mockDB.getUserFromEmail.return_value = None
    mockDB.getUserFromUsername.return_value = None

    response = service.signUp("valid@test.com", "validUser", "!invalidPass")
    
    assert not response["success"]
    assert response["message"] == "Password is not valid"

def test_signUp2():
    service, _, _ = get_service_and_mocks()
    
    response = service.signUp("valid@test.com", "!badUser", "validPassword123")
    
    assert not response["success"]
    assert "is not valid" in response["message"]

def test_signUp3():
    service, _, _ = get_service_and_mocks()
    
    response = service.signUp("notAnEmail", "validUser", "validPassword123")
    
    assert not response["success"]
    assert "is not valid" in response["message"]

def test_signUp4():
    service, mockDB, _ = get_service_and_mocks()
    
    mockDB.getUserFromEmail.return_value = {"username": "existingUser"}
    
    response = service.signUp("taken@test.com", "newUser", "validPassword123")
    
    mockDB.getUserFromEmail.assert_called_once_with("taken@test.com")
    assert not response["success"]
    assert response["message"] == "That email is taken"

def test_signUp5():
    service, mockDB, _ = get_service_and_mocks()
    
    mockDB.getUserFromEmail.return_value = None
    mockDB.getUserFromUsername.return_value = {"username": "takenUser"}
    
    response = service.signUp("free@test.com", "takenUser", "validPassword123")
    
    mockDB.getUserFromUsername.assert_called_once_with("takenUser")
    assert not response["success"]
    assert response["message"] == "That username is already taken"

@patch('bcrypt.hashpw')
def test_signUp_success(mock_hashpw):
    service, mockDB, _ = get_service_and_mocks()
    
    mockDB.getUserFromEmail.return_value = None
    mockDB.getUserFromUsername.return_value = None
    
    mock_hashpw.return_value = b"hashed_secret"
    
    email = "new@test.com"
    username = "newUser"
    password = "validPassword123"

    response = service.signUp(email, username, password)

    assert response["success"]
    assert response["message"] == "Successfully signed up"
    
    mockDB.addUser.assert_called_once_with(username, email, "hashed_secret")