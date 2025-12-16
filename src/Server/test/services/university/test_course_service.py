import pytest
from unittest.mock import Mock
from src.Server.services.university.course_service import CourseService

def get_service_and_mocks():
    mockDB = Mock()
    mockTokenService = Mock()
    service = CourseService(mockDB, mockTokenService)
    return service, mockDB, mockTokenService

def test_courseLookup1():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": False, 
        "message": "Token expired"
    }
    
    response = service.courseLookup("badToken", "CS", "1010", "Intro")
    
    assert not response["success"]
    assert response["message"] == "Token expired"
    
    mockDB.courseLookup.assert_not_called()

def test_courseLookup2():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mock_user = {"username": "student", "attends_university": 5}
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": mock_user
    }
    
    expected_courses = [
        {"id": 1, "code": "CS1010", "name": "Intro to CS"},
        {"id": 2, "code": "CS2020", "name": "Data Structures"}
    ]
    mockDB.courseLookup.return_value = expected_courses
    
    response = service.courseLookup("validToken", "CS", "1010", "Intro")
    
    assert response["success"] is True
    assert response["courses"] == expected_courses
    
    mockDB.courseLookup.assert_called_once_with(5, "CS", "1010", "Intro")

def test_courseLookup3():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"attends_university": 1}
    }
    
    mockDB.courseLookup.return_value = []
    
    response = service.courseLookup("validToken", "Art", "999", "Unknown")
    
    assert response["success"] is True
    assert response["courses"] == []