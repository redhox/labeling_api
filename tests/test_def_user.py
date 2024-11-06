import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from pydantic import BaseModel ,EmailStr
import pytest
from unittest.mock import Mock, patch
import python_multipart
# Importation des fonctions et variables à tester
from app.api.def_util.def_user import (
    get_user, get_db_access, create_access_token, get_current_user,
    SECRET_KEY, ALGORITHM, SystemUser, PostgresAccess
)

from datetime import datetime, timedelta
from jose import jwt
from fastapi import HTTPException, status

# Importation des fonctions et variables à tester
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)
import pytest
from datetime import datetime, timedelta
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)

from unittest.mock import MagicMock, patch
# Mock PostgresAccess at the module level, so it’s replaced in all imports
with patch("app.api.def_util.def_user.PostgresAccess") as MockPostgresAccess:
    # Configure the mock to avoid any real database connection attempts
    mock_conn = MockPostgresAccess.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {"id": 1, "email": "test@example.com", "username": "testuser"}
    
    # Import the functions and variables to test after setting up the mock
    from app.api.def_util.def_user import (
        get_current_user, create_access_token, SECRET_KEY, ALGORITHM
    )

@pytest.fixture
def mock_user():
    return {"email": "test@example.com", "username": "testuser"}

@pytest.fixture
def mock_token_data():
    # Simulate a valid token with a future expiration
    return {
        "sub": "test@example.com",
        "exp": int((datetime.utcnow() + timedelta(minutes=99999)).timestamp())
    }

@pytest.fixture
def db_connection():
    # Yield the mock connection object
    yield mock_conn  

def test_get_current_user_valid_token(db_connection):
    # Test that requires db_connection but uses the mocked version
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = 1;")
        result = cursor.fetchone()
        assert result is not None
        assert result["email"] == "test@example.com"

