import pytest
from unittest.mock import Mock
# Adjust import path
from src.Server.services.university.group_service import GroupService

# --- Helper ---
def get_service_and_mocks():
    mockDB = Mock()
    mockToken = Mock()
    service = GroupService(mockDB, mockToken)
    return service, mockDB, mockToken

# --- getGroupsForCourse Tests ---

def test_getGroupsForCourse_invalidToken():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {"valid": False, "message": "Expired"}
    
    response = service.getGroupsForCourse("badToken", "CS101")
    
    assert not response["success"]
    assert response["message"] == "Expired"
    mockDB.getGroupsForCourse.assert_not_called()

def test_getGroupsForCourse_success():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {"valid": True, "user": {"id": 1}}
    expected_groups = [{"id": 1, "name": "Study Group A"}]
    mockDB.getGroupsForCourse.return_value = expected_groups
    
    response = service.getGroupsForCourse("validToken", "CS101")
    
    assert response["success"]
    assert response["groups"] == expected_groups
    mockDB.getGroupsForCourse.assert_called_once_with("CS101")

# --- isGroupFull Tests ---

def test_isGroupFull_groupNotFound():
    service, mockDB, _ = get_service_and_mocks()
    
    # DB returns None for the group
    mockDB.getGroup.return_value = None
    
    response = service.isGroupFull("999")
    
    assert not response["success"]
    assert response["message"] == "Group does not exist"

def test_isGroupFull_true():
    service, mockDB, _ = get_service_and_mocks()
    
    # max_size 5, total_users 5 -> Should be FULL
    # NOTE: You must fix your logic (total_users >= max_size) for this to pass
    mockDB.getGroup.return_value = {"max_size": 5, "total_users": 5}
    
    response = service.isGroupFull("101")
    
    assert response["success"]
    assert response["isFull"] is True

def test_isGroupFull_false():
    service, mockDB, _ = get_service_and_mocks()
    
    # max_size 5, total_users 2 -> Should NOT be full
    mockDB.getGroup.return_value = {"max_size": 5, "total_users": 2}
    
    response = service.isGroupFull("101")
    
    assert response["success"]
    assert response["isFull"] is False

# --- joinGroup Tests ---

def test_joinGroup_invalidToken():
    service, mockDB, mockToken = get_service_and_mocks()
    mockToken.validateToken.return_value = {"valid": False, "message": "Invalid"}
    
    response = service.joinGroup("badToken", "123")
    
    assert not response["success"]

def test_joinGroup_groupDoesNotExist():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "student1"}
    }
    # Mock getGroup returning None (group not found)
    mockDB.getGroup.return_value = None
    
    response = service.joinGroup("validToken", "999")
    
    # NOTE: You must fix your return statement (return isGroupFullResponse) for this to pass
    assert not response["success"]
    assert response["message"] == "Group does not exist"
    
    # Ensure we didn't try to join
    mockDB.joinGroup.assert_not_called()

def test_joinGroup_isFull():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "student1"}
    }
    # Mock group being full (Users >= Max)
    mockDB.getGroup.return_value = {"max_size": 5, "total_users": 5}
    
    response = service.joinGroup("validToken", "101")
    
    assert not response["success"]
    assert response["message"] == "Group is full"
    mockDB.joinGroup.assert_not_called()

def test_joinGroup_success():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "student1"}
    }
    # Mock group having space (Users < Max)
    mockDB.getGroup.return_value = {"max_size": 5, "total_users": 3}
    
    response = service.joinGroup("validToken", "101")
    
    assert response["success"] is True
    
    # Verify DB interaction
    mockDB.joinGroup.assert_called_once_with("101", "student1")