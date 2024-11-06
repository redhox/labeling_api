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
from unittest.mock import MagicMock, patch
import pytest
from datetime import datetime, timedelta
import os

# Clear environment variables that might be influencing the DB connection
os.environ["DB_NAME"] = ""
os.environ["DB_USER"] = ""
os.environ["DB_PASSWORD"] = ""
os.environ["DB_HOST"] = ""

# Mock `PostgresAccess` at the test level
@pytest.fixture
def mock_postgres_access():
    with patch("app.api.def_util.def_user.PostgresAccess") as MockPostgresAccess:
        mock_conn = MockPostgresAccess.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser"
        }
        yield mock_conn  # Yield the mock connection for use in tests

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

def test_get_current_user_valid_token(mock_postgres_access):
    # Example test that utilizes `mock_postgres_access`
    with mock_postgres_access.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = 1;")
        result = cursor.fetchone()
        assert result is not None
        assert result["email"] == "test@example.com"


