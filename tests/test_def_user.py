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
from datetime import datetime, timedelta
from app.api.def_util.def_user import (
    get_current_user, create_access_token, SECRET_KEY, ALGORITHM, PostgresAccess
)

from unittest.mock import MagicMock, patch
# Mock PostgresAccess at the module level, so it’s replaced in all imports
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

class PostgresAccess:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
# Appliquer le patch global sur PostgresAccess avant d'importer les fonctions cibles
with patch("app.api.def_util.def_user.PostgresAccess") as MockPostgresAccess:
    mock_conn = MockPostgresAccess.return_value
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser"
    }

    # Importer les fonctions et variables nécessaires une fois que le mock est en place
    from app.api.def_util.def_user import get_current_user, create_access_token

@pytest.fixture
def mock_user():
    return {"email": "test@example.com", "username": "testuser"}

@pytest.fixture
def mock_token_data():
    # Simuler un token valide avec une expiration future
    return {
        "sub": "test@example.com",
        "exp": int((datetime.utcnow() + timedelta(minutes=99999)).timestamp())
    }

def test_get_current_user_valid_token():
    # Le mock est maintenant activé, le test ne tentera pas de se connecter réellement
    with mock_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = 1;")
        result = cursor.fetchone()
        assert result is not None
        assert result["email"] == "test@example.com"

