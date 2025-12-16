import pytest
from unittest.mock import Mock
from src.Server.services.university.university_service import UniversityService

def get_service_and_mocks():
    mockDB = Mock()
    mockTokenService = Mock()
    service = UniversityService(mockDB, mockTokenService)
    return service, mockDB, mockTokenService

def test_getUniversities1():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": False, 
        "message": "Token expired"
    }
    
    response = service.getUniversities("badToken")
    
    assert not response["success"]
    assert response["message"] == "Token expired"
    
    mockDB.getUniversities.assert_not_called()

def test_getUniversities2():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "testUser"}
    }
    
    expected_universities = [
        {"id": 1, "name": "University A"},
        {"id": 2, "name": "University B"}
    ]
    mockDB.getUniversities.return_value = expected_universities
    
    response = service.getUniversities("validToken")
    
    assert response["success"] is True
    assert response["universities"] == expected_universities
    
    mockDB.getUniversities.assert_called_once()

def test_joinUniversiy1():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {"valid": False, "message": "Invalid token"}
    
    response = service.joinUniversiy("badToken", 1)
    
    assert not response["success"]
    assert response["message"] == "Invalid token"
    
    mockDB.attends.assert_not_called()

def test_joinUniversiy2():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "student1"}
    }
    
    uni_id = 5
    
    response = service.joinUniversiy("validToken", uni_id)
    
    assert response["success"] is True
    
    mockDB.attends.assert_called_once_with("student1", uni_id)