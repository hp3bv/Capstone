import pytest
from unittest.mock import Mock
from datetime import datetime

from src.Server.services.authentication.auth_service import AuthService

def test_isValidEmail1():
    authService = AuthService(Mock(), Mock())
    assert authService.isValidEmail("test@test.com")
    
def test_isValidEmail2():
    authService = AuthService(Mock(), Mock())
    assert not authService.isValidEmail("testtest.com")
    
def test_isValidUsername():
    authService = AuthService(Mock(), Mock())
    assert authService.isValidUsername("testUser1")

def test_isValidUsername2():
    authService = AuthService(Mock(), Mock())
    assert not authService.isValidUsername("testUserOverTwentyChar")
    
def test_isValidUsername3():
    authService = AuthService(Mock(), Mock())
    assert not authService.isValidUsername("!testUser")
    
def test_isValidPassword1():
    authService = AuthService(Mock(), Mock())
    assert authService.isValidPassword("testPassword")
    
def test_isValidPassword2():
    authService = AuthService(Mock(), Mock())
    assert not authService.isValidPassword("testPasswordOverTwentyChar")
    
def test_isValidPassword3():
    authService = AuthService(Mock(), Mock())
    assert not authService.isValidPassword("!testPassword")
    
def test_hashPassword():
    authService = AuthService(Mock(), Mock())
    assert authService.hashPassword("testPassword") != "testPassword"

def test_success():
    authService = AuthService(Mock(), Mock())
    response = authService.success("testUser", "testMessage")
    assert response["success"]
    assert response["message"] == "testMessage"
    assert response["username"] == "testUser"
    
def test_failure():
    authService = AuthService(Mock(), Mock())
    response = authService.failure("testMessage")
    assert not response["success"]
    assert response["message"] == "testMessage"
    
def test_getUserFromUsername():
    mockDB = Mock()
    expectedUser = {
        "username": "test",
        "email": "test@test.com",
        "password_hash": "test_password_hash",
        "created_at": datetime.now(),
        "attends_university": 1
    }

    mockDB.getUserFromUsername.return_value = expectedUser
    service = AuthService(mockDB, Mock())

    result = service.retrieveUserFromUsername("test")

    mockDB.getUserFromUsername.assert_called_once_with("test")
    assert result == expectedUser
    
def test_getUserFromEmail():
    mockDB = Mock()
    expectedUser = {
        "username": "test",
        "email": "test@test.com",
        "password_hash": "test_password_hash",
        "created_at": datetime.now(),
        "attends_university": 1
    }

    mockDB.getUserFromEmail.return_value = expectedUser
    service = AuthService(mockDB, Mock())

    result = service.retrieveUserFromEmail("test@test.com")

    mockDB.getUserFromEmail.assert_called_once_with("test@test.com")
    assert result == expectedUser
