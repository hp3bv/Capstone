import pytest
from unittest.mock import Mock
from src.Server.services.message.message_service import MessageService

def get_service_and_mocks():
    mockDB = Mock()
    mockTokenService = Mock()
    service = MessageService(mockDB, mockTokenService)
    return service, mockDB, mockTokenService

def test_publishMessage_invalidToken():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": False, 
        "message": "Token expired"
    }
    
    response = service.publishMessage("badToken", "Hello World", 1)
    
    assert not response["success"]
    assert response["message"] == "Token expired"
    
    mockDB.addMessage.assert_not_called()

def test_publishMessage_contentTooLong():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "testUser"}
    }
    
    long_content = "a" * 1001
    
    response = service.publishMessage("validToken", long_content, 1)
    
    assert not response["success"]
    assert response["message"] == "Message is too long"
    mockDB.addMessage.assert_not_called()

def test_publishMessage_success():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "testUser"}
    }
    
    mockDB.getGroup.return_value = {"group_id": 1}
    
    mockDB.addMessage.return_value = 101
    
    content = "Hello world"
    response = service.publishMessage("validToken", content, 1)
    
    assert response["success"]
    assert response["message"] == "Successfully published"
    assert response["messageId"] == 101
    
    mockDB.addMessage.assert_called_once_with("testUser", content, 1)

def test_getMessages_invalidToken():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {"valid": False, "message": "Invalid token"}
    
    response = service.getMessages("badToken", 1)
    
    assert not response["success"]
    assert response["message"] == "Invalid token"
    mockDB.getMessages.assert_not_called()

def test_getMessages_success():
    service, mockDB, mockToken = get_service_and_mocks()
    
    mockToken.validateToken.return_value = {
        "valid": True, 
        "user": {"username": "testUser"}
    }

    mockDB.getGroup.return_value = {"group_id": 1}
    
    expected_messages = [
        {"id": 1, "content": "Hi", "username": "alice"},
        {"id": 2, "content": "Hello", "username": "bob"}
    ]
    mockDB.getMessages.return_value = expected_messages
    
    response = service.getMessages("validToken", 1)
    
    assert response["success"]
    assert response["messages"] == expected_messages
    
    mockDB.getMessages.assert_called_once_with(1)