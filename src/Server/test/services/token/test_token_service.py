import pytest
from unittest.mock import Mock, patch
from jose import jwt
import os

from src.Server.services.token.token_service import TokenService

TEST_SECRET = "testing_secret_key"
ALGORITHM = "HS256"

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def token_service(mock_db):
    with patch.dict(os.environ, {"KEY": TEST_SECRET}):
        return TokenService(mock_db)

def test_init_raises_error_if_no_key():
    mock_db = Mock()
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="KEY not set"):
            TokenService(mock_db)

def test_init_success_with_key():
    mock_db = Mock()
    with patch.dict(os.environ, {"KEY": TEST_SECRET}):
        service = TokenService(mock_db)
        assert service.secretKey == TEST_SECRET

def test_createToken(token_service):
    username = "testUser"
    token = token_service.createToken(username)
    
    assert isinstance(token, str)
    
    payload = jwt.decode(token, TEST_SECRET, algorithms=[ALGORITHM])
    assert payload["sub"] == username

def test_validateToken1(token_service, mock_db):
    username = "testUser"
    
    token = jwt.encode({"sub": username}, TEST_SECRET, algorithm=ALGORITHM)
    
    expected_user = {"username": username, "id": 1}
    mock_db.getUserFromUsername.return_value = expected_user
    
    result = token_service.validateToken(token)
    
    assert result["valid"] is True
    assert result["user"] == expected_user
    mock_db.getUserFromUsername.assert_called_once_with(username)

def test_validateToken2(token_service, mock_db):
    wrong_secret_token = jwt.encode({"sub": "testUser"}, "WRONG_KEY", algorithm=ALGORITHM)
    
    result = token_service.validateToken(wrong_secret_token)
    
    assert result["valid"] is False
    assert result["message"] == "Token is invalid or expired"
    mock_db.getUserFromUsername.assert_not_called()

def test_validateToken3(token_service, mock_db):
    malformed_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid_payload.signature"
    
    result = token_service.validateToken(malformed_token)
    
    assert result["valid"] is False
    assert result["message"] == "Token is invalid or expired"

def test_validateToken4(token_service, mock_db):
    token = jwt.encode({"sub": "ghostUser"}, TEST_SECRET, algorithm=ALGORITHM)
    
    mock_db.getUserFromUsername.return_value = None
    
    result = token_service.validateToken(token)
    
    assert result["valid"] is False
    assert result["message"] == "User not found"
    mock_db.getUserFromUsername.assert_called_once_with("ghostUser")

def test_validateToken5(token_service, mock_db):
    token = jwt.encode({"not_sub": "value"}, TEST_SECRET, algorithm=ALGORITHM)
    
    result = token_service.validateToken(token)
    
    assert result["valid"] is False
    assert result["message"] == "Token is invalid or expired"